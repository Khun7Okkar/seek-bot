import pandas as pd
import os
import config

def convert_excel_to_md(input_filename="jobs_found.xlsx", output_filename="jobs_report.md"):
    input_file = os.path.join(config.DATA_DIR, input_filename)
    output_file = os.path.join(config.DATA_DIR, output_filename)
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found. Please run main.py first.")
        return

    try:
        df = pd.read_excel(input_file)
        
        # Create markdown content
        md_content = "# Job Search Report\n\n"
        
        # Add summary stats
        md_content += f"**Total Jobs Found:** {len(df)}\n"
        md_content += f"**Generated:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        
        # Iterate through jobs and format nicely
        for index, row in df.iterrows():
            company = row.get('Company', 'N/A')
            position = row.get('Job Position', 'N/A')
            date_posted = row.get('Date posted', 'N/A')
            link = row.get('Link to post', '#')
            description = row.get('Full Job Description', 'No description available.')
            
            md_content += f"## {index + 1}. {position} at {company}\n"
            md_content += f"- **Date Posted:** {date_posted}\n"
            md_content += f"- **Link:** [View Job Post]({link})\n\n"
            md_content += "### Description\n"
            md_content += f"{description}\n\n"
            md_content += "---\n\n"

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(md_content)
            
        print(f"Success! Converted to {output_file}")
            
    except Exception as e:
        print(f"Error converting file: {e}")

if __name__ == "__main__":
    convert_excel_to_md()
