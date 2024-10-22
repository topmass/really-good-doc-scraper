import asyncio
import os
from urllib.parse import urlparse
from crawlee.playwright_crawler import PlaywrightCrawler, PlaywrightCrawlingContext
import csv
import argparse

def clean_domain(url):
    """Clean domain name for folder/file naming"""
    domain = urlparse(url).netloc
    return domain.replace('www.', '').replace('.', '')

def sanitize_filename(url):
    """Sanitize URL for filename"""
    parsed = urlparse(url)
    # Remove scheme (http/https) and domain
    path = parsed.path + parsed.params + parsed.query
    return "".join(x for x in path if x.isalnum() or x in ['-', '_']).rstrip()

class WebsiteScraper:
    def __init__(self, start_url):
        self.start_url = start_url
        self.base_domain = urlparse(start_url).netloc
        self.visited_urls = set()
        self.domain_folder = clean_domain(start_url)
        
        # Create domain-specific folders
        self.md_folder = os.path.join("scraped_pages", self.domain_folder)
        self.csv_folder = "url_list"
        os.makedirs(self.md_folder, exist_ok=True)
        os.makedirs(self.csv_folder, exist_ok=True)
        
        self.crawler = PlaywrightCrawler()
        
        @self.crawler.router.default_handler
        async def handle_page(context: PlaywrightCrawlingContext):
            url = context.request.url
            if url in self.visited_urls:
                return

            self.visited_urls.add(url)
            context.log.info(f'Processing {url}...')
            
            try:
                await context.page.wait_for_load_state('networkidle')
                
                content = await context.page.evaluate('''
                    () => {
                        // Remove unwanted elements
                        const elementsToRemove = document.querySelectorAll(`
                            script, style, iframe,
                            header, footer,
                            [role="banner"],
                            [role="contentinfo"],
                            nav,
                            .header, .footer, .nav,
                            #header, #footer, #nav,
                            .navigation, #navigation,
                            .menu, #menu,
                            .sidebar, #sidebar,
                            [class*="header"], 
                            [class*="footer"],
                            [class*="navigation"]
                        `);
                        
                        elementsToRemove.forEach(el => el.remove());
                        
                        // Get the main content
                        const mainContent = document.querySelector('main, [role="main"], article, .content, #content') || document.body;
                        
                        // Helper function to process text content
                        function processNode(node) {
                            let result = '';
                            
                            // Handle headings
                            if (node.tagName && node.tagName.match(/^H[1-6]$/)) {
                                const level = node.tagName[1];
                                return '\\n' + '#'.repeat(level) + ' ' + node.textContent.trim() + '\\n\\n';
                            }
                            
                            // Handle paragraphs and other block elements
                            if (node.tagName && ['P', 'DIV', 'SECTION', 'ARTICLE'].includes(node.tagName)) {
                                return '\\n' + node.textContent.trim() + '\\n\\n';
                            }
                            
                            // Handle lists
                            if (node.tagName === 'LI') {
                                return '* ' + node.textContent.trim() + '\\n';
                            }
                            
                            // Process child nodes
                            node.childNodes.forEach(child => {
                                if (child.nodeType === 3) { // Text node
                                    result += child.textContent.trim() + ' ';
                                } else if (child.nodeType === 1) { // Element node
                                    result += processNode(child);
                                }
                            });
                            
                            return result;
                        }
                        
                        return processNode(mainContent)
                            .replace(/\\n\\s*\\n\\s*\\n/g, '\\n\\n') // Remove extra blank lines
                            .trim();
                    }
                ''')
                
                # Save content with original markdown formatting
                sanitized_url = sanitize_filename(url)
                if sanitized_url == "":
                    sanitized_url = "index"
                    
                with open(f"{self.md_folder}/{sanitized_url}.md", "w", encoding="utf-8") as f:
                    f.write(f"# {url}\n\n{content}")

                # Save URLs to domain-specific CSV
                csv_filename = f"{self.domain_folder}_urls.csv"
                with open(os.path.join(self.csv_folder, csv_filename), "a", newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([url])

                await context.enqueue_links()
                
            except Exception as e:
                context.log.error(f"Error processing {url}: {str(e)}")

    async def run(self):
        await self.crawler.run([self.start_url])

async def main():
    parser = argparse.ArgumentParser(description='Web scraper for any website')
    parser.add_argument('url', help='Starting URL to scrape (e.g., https://example.com)')
    
    args = parser.parse_args()
    scraper = WebsiteScraper(args.url)
    await scraper.run()

if __name__ == "__main__":
    asyncio.run(main())