import requests as r
from bs4 import BeautifulSoup as bs
from fpdf import FPDF



# Making request to the hackernews website
response = r.get('https://news.ycombinator.com/news')
soup = bs(response.text, 'html.parser')
# print(soup.prettify())
# print(soup.body.prettify())
links =  soup.select('.titleline > a')
votes = soup.select('.score')


def create_custom_hn(links, votes):
    hn = []
    for index, item in enumerate(links):
        title = links[index].getText()
        href = links[index].get('href', None)
        points = int(votes[index].getText().replace(' points', ''))
        if points > 50:
            hn.append({'title': title, 'link': href, 'votes': points})
    return hn

def create_pdf(hn):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    
    for item in hn:
        title = item['title']
        link = item['link']
        votes = str(item['votes'])
        
        # Convert the title and link to UTF-8 encoding
        title = title.encode('latin-1', 'replace').decode('latin-1')
        link = link.encode('latin-1', 'replace').decode('latin-1')
        
        pdf.multi_cell(0, 10, txt=f"Title: {title}", align='L')
        pdf.multi_cell(0, 10, txt=f"Link: {link}", align='L')
        pdf.multi_cell(0, 10, txt=f"Votes: {votes}", align='L')
        pdf.ln(10)  # line break
    
    pdf.output("hn_results.pdf")

hn = create_custom_hn(links, votes)

create_pdf(hn)