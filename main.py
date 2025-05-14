
from document_handler import DocumentHandler
handler = DocumentHandler()
import uuid
languages=['ru', 'uz']
project_id = 'osnova'
data = """
Osnova - sizning karyerangiz bo‘yicha ko‘makchingiz. Biz sizga kasb tanlashda yordam beramiz, zamonaviy bilim va ko‘nikmalar beramiz, yetakchi kompaniyalar bilan tanishtirамiz hamda professional jamiyatning a’zosiga aylantiramiz. Biz yangi kasblarga o‘rgatamiz, ko‘nikmalarni rivojlantiramiz, o‘z yo‘lingizni tanlashga va zamonaviy karyera qurishga ko‘maklashamiz.
"""

DocumentHandler().data_upload(project_id=project_id, row_data=data, languages=languages)



product_details = {
    "name": "HR maktabi",
    "details": {"description": """   
Kurs HR menejmentining asosiy jihatlarini qamrab oladi: tashkiliy tuzilma va biznes jarayonlarini shakllantirishdan tortib, xodimlarni ishga qabul qilish, moslashtirish va rag‘batlantirishgacha. Yumshoq ko‘nikmalar va raqamli vositalar bilan ishlashga alohida e’tibor qaratiladi (Microsoft Office, MyMehnat, 1C). Siz HR strategiyalari biznesga qanday ta’sir ko‘rsatishi va ularni turli tashkilotlarda samarali qo‘llash haqida tushunchaga ega bo‘lasiz.
""",
    "price" : '1000000 sum',
    "link": "https://osnovaeducation.uz/hr_school"
    },
    "id": uuid.uuid4().hex,
    "languages": languages
}
DocumentHandler().create_product(details=product_details, project_id=project_id, lang='uz')

product_details["details"]["price"] = "2000000 sum"

DocumentHandler().update_product(details=product_details, project_id=project_id, lang='uz')

# # Get a product from the vector database
product_id = product_details['id']
product = DocumentHandler().get_product(project_id=project_id, product_id=product_id, languages=languages)

# DocumentHandler().delete_product(project_id=project_id, product_id=product_id, languages=languages)


while True:
    query = input("Enter your query: ")
    if query.lower() == "exit":
        break


    question_details = {
        "history": [],
        "user_question": query,
        "project_name": project_id,
        "project_id": project_id,
        "lang": 'uz',
        "company_data": "Osnova - sizning karyerangiz bo‘yicha ko‘makchingiz.",
        "service_type": "support"
    }
    result = DocumentHandler().ask_question(question_details=question_details)
    print(f"{'-'*30} \n{result}\n {'-'*30}")