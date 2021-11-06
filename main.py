from bs4 import BeautifulSoup
import requests


search_term = input("Ce vrei sa cauti? ")
url = f"https://www.emag.ro/search/stoc/{search_term}"
page = requests.get(url).text
doc = BeautifulSoup(page, "html.parser")

#  cate pagini are cautarea!!
page_text = doc.find(class_="visible-xs visible-sm")
pages = int(str(page_text).split("din")[-1].split("<")[0])

products_np = []
products_link = []

#  loop pe fiecare pagina !!
for page in range(1, pages + 1):
    url = f"https://www.emag.ro/search/stoc/{search_term}/p{page}"
    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")

# gasire link catre produs !!
    item_link = doc.find_all(class_="card-v2-info")
    for i in item_link:
        link = str(i.contents)
        ll = link.find("href")
        lf = link.find('>')
        links = link[ll + 6:lf - 1]
        check = {"LINK": links}
        products_link.append(check)

# gasie nume produs !!
    soup = doc.find_all(class_="card-v2-toolbox")
    for i in soup:
        name = str(i.contents)
        pnl = name.find("product_name")
        pnf = name.find("options_modal")
        product_name = name[pnl + 15:pnf - 3]

# gasire pret produs !!
        pricel = name.find("price")
        pricef = name.find("category_trail")
        product_price = name[pricel + 7:pricef - 2] + " lei"
        products = {"NUME": product_name, "PRET": product_price}
        products_np.append(products)

result = zip(products_np, products_link)
for i in result:
    print(i)
