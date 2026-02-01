import asyncio
import pandas as pd
import config
from browser_agent import BrowserAgent
from extractor import JobExtractor
from datetime import datetime

async def main():
    print("=== Local-First Agentic Job Searcher Started ===")
    
    agent = BrowserAgent()
    extractor = JobExtractor()
    
    all_jobs = []
    
    await agent.start()
    
    try:
        for role in config.JOB_ROLES:
            print(f"\nScanning for Role: {role} in {config.LOCATION}")
            
            if config.SITES["SEEK"]:
                print("--- Checking SEEK ---")
                try:
                    await agent.search_seek(role, config.LOCATION)
                    
                    # NOTE: In a real scraper, we'd iterate over result links.
                    # For this V1, let's assume we are on the results page and parsing *that* 
                    # OR we need to collect links and visit them.
                    # As per "Browser Agent" description: "browse job boards... analyze job postings".
                    # To effectively get descriptions, usually need to visit individual pages.
                    # Let's implement a simple "get detail pages" loop here or in agent.
                    
                    # For V1 simplicity scaffolding: 
                    # 1. We are on result page.
                    # 2. Extract links (using a reliable selector or getting all 'a' tags with specific text).
                    # 3. Visit first X links.
                    
                    # Let's simple-hack: Grab all links that look like job posts.
                    # Seek hrefs usually contain '/job/'
                    
                    # Get links from current page
                    page_links = await agent.page.evaluate("""
                        () => Array.from(document.querySelectorAll('a[href*="/job/"]')).map(a => a.href)
                    """)
                    
                    # Deduplicate
                    page_links = list(set(page_links))
                    print(f"  Found {len(page_links)} potential job links on first page.")
                    
                    # Limit to first few for testing/speed
                    for i, link in enumerate(page_links[:5]): 
                        print(f"  Processing {i+1}/{len(page_links[:5])}: {link}")
                        try:
                            await agent.navigate_to(link)
                            html = await agent.get_page_content()
                            
                            job_data = extractor.extract_job_details(html)
                            
                            if job_data:
                                job_data['Link to post'] = link
                                job_data['S.N'] = len(all_jobs) + 1
                                all_jobs.append(job_data)
                                print(f"    -> Extracted: {job_data.get('job_position', 'N/A')} at {job_data.get('company_name', 'N/A')}")
                            
                        except Exception as e:
                            print(f"    Failed to process link {link}: {e}")
                            
                except Exception as e:
                    print(f"Seek search failed: {e}")

            if config.SITES["LINKEDIN"]:
                # Similar logic for LinkedIn would go here
                pass

    finally:
        await agent.stop()
        
    # Save to Excel
    print(f"\nFormatting and saving {len(all_jobs)} jobs to Excel...")
    if all_jobs:
        df = pd.DataFrame(all_jobs)
        
        # reorder columns
        cols = ['S.N', 'company_name', 'job_position', 'full_description', 'Link to post', 'date_posted']
        # Map JSON keys to Config columns where they differ
        # JSON: company_name, job_position, full_description, date_posted
        # Config req: S.N, Company, Job Position, Full Job Description, Link to post, Date posted
        
        df = df.rename(columns={
            'company_name': 'Company',
            'job_position': 'Job Position',
            'full_description': 'Full Job Description',
            'date_posted': 'Date posted'
        })
        
        # Ensure strict column order if keys exist
        available_cols = [c for c in ['S.N', 'Company', 'Job Position', 'Full Job Description', 'Link to post', 'Date posted'] if c in df.columns]
        df = df[available_cols]

        import os
        if not os.path.exists(config.DATA_DIR):
            os.makedirs(config.DATA_DIR)
            
        filename = os.path.join(config.DATA_DIR, "jobs_found.xlsx")
        try:
            # Use xlsxwriter for formatting
            with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')
                workbook = writer.book
                worksheet = writer.sheets['Sheet1']
                
                # Format Description column (D is index 3)
                wrap_format = workbook.add_format({'text_wrap': True})
                worksheet.set_column('D:D', 60, wrap_format) # Wide column for desc
                
            print(f"Success! Saved to {filename}")
        except Exception as e:
            print(f"Error saving Excel: {e}")
            # Fallback
            df.to_excel(os.path.join(config.DATA_DIR, "jobs_found_backup.xlsx"))

if __name__ == "__main__":
    asyncio.run(main())
