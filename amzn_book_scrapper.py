from bs4 import BeautifulSoup
import requests
import pandas as pd
import time


def store_data(information_map):
    df = pd.DataFrame.from_dict(information_map) 
    df.to_csv (r'amzn_books.csv', index = False, header=True)

def get_author(soup):
    try:
        authorname=soup.find('a',attrs={'class':"a-link-normal contributorNameID"})
        return authorname.string
    except:
        return "NULL"

def get_page(soup):
    pass
# Function to extract Product Title
def get_title(soup):
	
	try:
		title = soup.find("span", attrs={"id":'productTitle'})
		title_value = title.string
		title_string = title_value.strip()
  
	except AttributeError:
		title_string = "NULL"	

	return title_string

# Function to extract Product Price
def get_price(soup):

	try:
		price = soup.find("span", attrs={'class':'a-size-base a-color-price a-color-price'}).string.strip()


	except AttributeError:

		try:
			# If there is some deal price
			price = soup.find("span", attrs={'id':'priceblock_dealprice'}).string.strip()

		except:		
			price = "NULL"	

	return price

# Function to extract Product Rating
def get_rating(soup):

	try:
		rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
		
	except AttributeError:
		
		try:
			rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
		except:
			rating = "NULL"	

	return rating

# Function to extract Number of User Reviews
def get_review_count(soup):
	try:
		review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()
		
	except AttributeError:
		review_count = "NULL"	

	return review_count

# Function to extract Availability Status
def get_availability(soup):
	try:
		available = soup.find("div", attrs={'id':'availability'})
		available = available.find("span").string.strip()

	except AttributeError:
		available = "Not Available"	

	return available	

def extract_info(soups):
    links = soups.find_all('a', attrs={'class':'a-link-normal'})
    links_list = []

    for link in links:
        links_list.append(link.get('href'))
    links_list = [*set(links_list)]

    print(links_list,sep='\n')
    for i in links_list:      
        try:  
            time.sleep(1)
            req=requests.get(base_link+i,headers=headers)

            if req.status_code < 500:
                soup = BeautifulSoup(req.content, 'html.parser')
                if get_title(soup)=='NULL':
                    continue
                title.append(get_title(soup))
                product_link.append(base_link+i)

                author_name.append(get_author(soup))
                availability.append(get_availability(soup))
                price_list.append(get_price(soup))
                rating.append(get_rating(soup))
                review_count_list.append(get_review_count(soup))
                req.close()
            else:
                print("Link opening error : 404")
                
        
        except:
            print("no")
                

if __name__ == '__main__':
    global price_list
    global title
    global author_name
    global page
    global availability
    global rating
    global review_count_list
    global product_link
    global base_link
    
    global headers
    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.in/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }
    product_link=list()
    price_list=list()
    title=list()
    author_name=list()
    page=list()
    availability=list()
    rating=list()
    review_count_list=list()
    
    
    base_link='https://www.amazon.in'
    target_link='https://www.amazon.in/gp/bestsellers/books/ref=zg_bs_pg_1?ie=UTF8&pg='

    for i in range(1,9):
        try:
            req=requests.get(target_link+str(i),headers=headers)
            
            soup = BeautifulSoup(req.content, 'html.parser')
            
            extract_info(soup)
            req.close()
        except:
            print("Error connecting")
            quit()
	
    information_map={'Title':title,'Price':price_list,'Author Name':author_name,'Availability':availability,'Rating':rating,'Review Count':review_count_list,'Link':product_link}
    store_data(information_map)
    
  
  
