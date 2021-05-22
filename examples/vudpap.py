from docflow import APIClient, APIClientFileExistsException, APIClientDocumentException
from io import BytesIO
from zipfile import ZipFile
from tempfile import NamedTemporaryFile
import requests


files2 = [
    "https://vudpap.sk/wp-content/uploads/2021/02/FA-1-8-2021.zip",
    "https://vudpap.sk/wp-content/uploads/2021/03/FA-9-19-2021.zip",
    "https://vudpap.sk/wp-content/uploads/2021/03/FA-20-30-2021.zip",
    "https://vudpap.sk/wp-content/uploads/2021/03/FA-31-41-2021.zip",
    "https://vudpap.sk/wp-content/uploads/2021/03/FA-42-52-2021.zip",
    "https://vudpap.sk/wp-content/uploads/2021/04/FA-53-69-2021.zip",
    "https://vudpap.sk/wp-content/uploads/2021/05/FA-70-78-2021.zip",
    "https://vudpap.sk/wp-content/uploads/2021/03/FA-NPS-1-19-2021.zip",
    "https://vudpap.sk/wp-content/uploads/2021/03/FA-NPS-20-43-2021.zip",
    "https://vudpap.sk/wp-content/uploads/2021/03/FA-NP-44-60-2021.zip",
    "https://vudpap.sk/wp-content/uploads/2021/03/FA-NP-61-73-2021.zip",
    "https://vudpap.sk/wp-content/uploads/2021/04/FA-NP-74-105-2021.zip",
    "https://vudpap.sk/wp-content/uploads/2021/04/FA_01_2021.zip",
    "https://vudpap.sk/wp-content/uploads/2021/04/FA_02_2021.zip",
    "https://vudpap.sk/wp-content/uploads/2021/04/FA_03_2021.zip",
    "https://vudpap.sk/wp-content/uploads/2021/05/FA-UPP-04.2021.zip",
    "https://vudpap.sk/wp-content/uploads/2020/01/FA-1-10-2020.zip",
    "https://vudpap.sk/wp-content/uploads/2020/01/FA-11-20-2020.zip",
    "https://vudpap.sk/wp-content/uploads/2020/02/Faktúry-21-35-2020.zip",
    "https://vudpap.sk/wp-content/uploads/2020/02/Faktúry-36-44-2020.zip",
    "https://vudpap.sk/wp-content/uploads/2020/03/Faktúry-45-52-2020.zip",
    "https://vudpap.sk/wp-content/uploads/2020/03/Faktúry-53-61-2020.zip",
    "https://vudpap.sk/wp-content/uploads/2020/03/Faktúry-62-80-2020.zip",
    "https://vudpap.sk/wp-content/uploads/2020/04/Faktúry-81-94-2020.zip",
    "https://vudpap.sk/wp-content/uploads/2020/04/FA-95-104-2020.zip",
    "https://vudpap.sk/wp-content/uploads/2020/05/FA-105-113-2020.zip",
    "https://vudpap.sk/wp-content/uploads/2020/05/FA-114-121-2020.zip",
    "https://vudpap.sk/wp-content/uploads/2020/06/Faktúry-122-140-2020.zip",
    "https://vudpap.sk/wp-content/uploads/2020/07/FA-142-155-2020.zip",
    "https://vudpap.sk/wp-content/uploads/2020/08/FA-160-161-2020.zip",
    "https://vudpap.sk/wp-content/uploads/2020/08/FA-162-178-2020.zip",
    "https://vudpap.sk/wp-content/uploads/2020/09/FA-179-189-2020.zip",
    "https://vudpap.sk/wp-content/uploads/2020/10/FA-190-196-2020.zip",
    "https://vudpap.sk/wp-content/uploads/2020/10/FA-197-207-2020.zip",
    "https://vudpap.sk/wp-content/uploads/2020/11/FA-208-215-2020.zip",
    "https://vudpap.sk/wp-content/uploads/2020/12/FA-216-226-2020.zip",
    "https://vudpap.sk/wp-content/uploads/2020/12/FA-227-235-2020-fix.zip",
    "https://vudpap.sk/wp-content/uploads/2020/12/FA-236-246-2020.zip",
    "https://vudpap.sk/wp-content/uploads/2020/12/FA-247-253-2020.zip",
    "https://vudpap.sk/wp-content/uploads/2021/01/FA-254-259-2020.zip",
    "https://vudpap.sk/wp-content/uploads/2021/01/FA-260-261-2020.zip",
    "https://vudpap.sk/wp-content/uploads/2020/02/Faktúry-NP-1-13-2020.zip",
    "https://vudpap.sk/wp-content/uploads/2020/02/Faktúry-NP-14-30-2020.zip",
    "https://vudpap.sk/wp-content/uploads/2020/03/Faktúry-NP-30-50-2020.zip",
    "https://vudpap.sk/wp-content/uploads/2020/03/Faktúry-NP-51-61-2020.zip",
    ]
files = [
    "https://vudpap.sk/wp-content/uploads/2020/04/FA-NP-62-72-2020.zip",
    "https://vudpap.sk/wp-content/uploads/2020/04/FA-NP-73-82-2020.zip",
    "https://vudpap.sk/wp-content/uploads/2020/06/Faktúry-NP-83-104-2020-fix.zip",
    "https://vudpap.sk/wp-content/uploads/2020/06/Faktúry-NP-105-115-2020.zip",
    "https://vudpap.sk/wp-content/uploads/2020/06/Faktúry-NP-116-127-2020.zip",
    "https://vudpap.sk/wp-content/uploads/2020/08/FA-NP-140-150-2020.zip",
    "https://vudpap.sk/wp-content/uploads/2020/08/FA-NP-151-160-2020.zip",
    "https://vudpap.sk/wp-content/uploads/2020/09/FA-NP-161-170-2020.zip",
    "https://vudpap.sk/wp-content/uploads/2020/09/FA-NP-171-180-2020.zip",
    "https://vudpap.sk/wp-content/uploads/2020/09/FA-NP-181-190-2020.zip",
    "https://vudpap.sk/wp-content/uploads/2020/09/FA-NP-191-205-2020.zip",
    "https://vudpap.sk/wp-content/uploads/2020/10/FA-NP-206-215-2020.zip",
    "https://vudpap.sk/wp-content/uploads/2020/10/FA-NP-216-230-2020.zip",
    "https://vudpap.sk/wp-content/uploads/2020/10/FA-NP-231-241-2020.zip",
    "https://vudpap.sk/wp-content/uploads/2020/11/FA-NP-242-250-2020.zip",
    "https://vudpap.sk/wp-content/uploads/2020/11/FA-NP-251-260-2020.zip",
    "https://vudpap.sk/wp-content/uploads/2020/11/FA-NP-261-270-2020.zip",
    "https://vudpap.sk/wp-content/uploads/2020/12/FA-NPS-280-306-2020.zip",
    "https://vudpap.sk/wp-content/uploads/2021/01/FA-NP-309-337-2020.zip",
    "https://vudpap.sk/wp-content/uploads/2021/01/FA-NP-338-346-2020.zip",
    "https://vudpap.sk/wp-content/uploads/2021/01/FA-EZS-1-5-2020.zip",
    "https://vudpap.sk/wp-content/uploads/2020/01/Faktúry-75-96-2019.zip",
    "https://vudpap.sk/wp-content/uploads/2020/01/Faktúry-97-124-2019.zip",
    "https://vudpap.sk/wp-content/uploads/2020/01/Faktúry-125-149-2019.zip",
    "https://vudpap.sk/wp-content/uploads/2020/01/Faktúry-150-162-2019.zip",
    "https://vudpap.sk/wp-content/uploads/2020/01/Faktúry-163-177-2019.zip",
    "https://vudpap.sk/wp-content/uploads/2020/01/Faktúry-178-204-2019.zip",
    "https://vudpap.sk/wp-content/uploads/2020/01/Faktúry-205-229-2019.zip",
    "https://vudpap.sk/wp-content/uploads/2020/01/Faktúry-230-263-2019.zip",
    "https://vudpap.sk/wp-content/uploads/2019/11/Faktury-NP-1-5-2019.zip",
    "https://vudpap.sk/wp-content/uploads/2020/02/Faktúry-NP-6-23-2019.zip",
    "https://vudpap.sk/wp-content/uploads/2020/02/Faktúry-NP-24-43-2019.zip",
    "https://vudpap.sk/wp-content/uploads/2020/01/Faktúry-NP-44-80-2019.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-1-22-2018.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-23-49-2018.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-50-94-2018.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-95-125-2018.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-126-136-2018.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-137-147-2018.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-148-163-2018.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-166-182-2018.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-183-197-2018.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-199-226-2018.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-227-260-2018.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-261-298-2018.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-1-50-2017.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-51-100-2017.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-101-149-2017.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-151-200-2017.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-201-245-2017.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-1-50-2016.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-51-100-2016.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-101-150-2016.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-151-200-2016.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-201-250-2016.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-251-284-2016.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-1-50-2015.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-51-100-2015.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-101-150-2015.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-151-202-2015.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-ESF-61570001-61570118-2015.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-ESF-61570119-61570226-2015.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-ESF-61570229-61570325-2015.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Ref.-CN-61570155-71570365-2015.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Ref.-CN-71570377-71570207-2015.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-1-50-2014.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-51-100-2014.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-101-150-2014.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-151-200-2014.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-201-226-2014.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-ESF-61470001-61470052-2014.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-ESF-61470053-61470102-2014.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-ESF-61470103-61470156-2014.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-ESF-61470157-61470207-2014.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-ESF-61470208-61470258-2014.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-ESF-61470259-61470316-2014.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Ref.-CN-71470068-71470435-2014.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Ref.-CN-71470436-71470524-2014.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-1-50-2013.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-51-100-2013.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-101-150-2013.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-151-200-2013.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-201-250-2013.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-252-290-2013.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-ESF-61370001-61370038_2013.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-ESF-61370039-61370070-2013.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-1-50-2012.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-51-100-2012.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-101-150-2012.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-151-200-2012.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-201-250-2012.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-251-267-2012.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-1-30-2011.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-31-60-2011.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-61-90-2011.zip",
    "https://vudpap.sk/wp-content/uploads/2019/01/Faktúry-91-246-2011.zip"
]


files_dir = "files_novemesto/*.pdf"
email = "branislav@vaculciak.sk"
password = "spustiwacco"
owner_id = "609cd3dba21b87c7152913cd"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

with APIClient(email=email, password=password, owner_id=owner_id) as api:
    print(api.is_logged_in())
    print(api.get_document_types())

    for zip_url in files:
        print("url:", zip_url)
        resp = requests.get(zip_url, stream=True, headers=headers)
        if resp.status_code == 200:
            with ZipFile(BytesIO(resp.content)) as zf:
                for file_name in zf.namelist():
                    tmp = NamedTemporaryFile(mode='w+b')
                    tmp.write(zf.read(file_name))
                    tmp.seek(0)

                    try:
                        api.upload_document(tmp.name, file_name=file_name, type='incomingInvoice', split_pages=False, exception_if_exists=True)
                        tmp.close()
                    except APIClientFileExistsException as e:
                        print(e.message)
                    except APIClientDocumentException as e:
                        print(e.message)
                    except Exception as e:
                        print(e)

