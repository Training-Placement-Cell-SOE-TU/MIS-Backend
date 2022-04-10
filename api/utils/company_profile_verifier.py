import requests
def validate_company_profile(company):
        """Validates compnay name
            Criteria:
                -> Company should have it's own page on LinkedIn    
        """

        company = company.replace(' ','').lower()
        url = f"https://www.linkedin.com/company/{company}"

        payload={}
        headers = {
            'authority': 'www.linkedin.com',
            'method': 'GET',
            'path': '/company/verizon/',
            'scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': 'li_sugr=a9ec4480-7d0c-4845-95e7-39605d64191e; bcookie="v=2&8aaee4d9-dae2-4557-8982-764a1c4d8220"; bscookie="v=1&2022011215585042776796-5cc9-45a6-8cc5-81319174ccc1AQE_17iC6_72LTD8_p-00jJCspROFjDQ"; lang=v=2&lang=en-us; _gcl_au=1.1.417085013.1642018060; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; aam_uuid=15799541411558395992045813087850080675; li_rm=AQFw0wobjO2NlAAAAX5P55PV9VBojDJkqKhl_YRquLswhB18wxW5CrzlKEbyd4a5Pkzg4sK4titxilH1vTM4uvdtNP51lhhdj3SPrI211t6J-s-eGf37cdyS; li_at=AQEDASpjhLADRqWwAAABfk_nnOUAAAF-c_Qg5U4Avoa3chQYq0gbZXsytq09SlpZZBggeNaQsXJ02AQ5fAJyV5Yq9vn0rTQoAszAKcsdg6bsVo-UHJcwisQGyxpLp3mVYESTXOa5hPbmf6Ba5Hr6g389; liap=true; JSESSIONID="ajax:8815064273025167449"; timezone=Asia/Calcutta; _guid=271bb573-1864-4058-8892-8bd0c8593a8d; AnalyticsSyncHistory=AQK2_sag26JQDQAAAX5P561HnSsDCdtE74-2dCE4vAO3tTg5oP08xO1DW6TitJ7n2Ipoaqxx28Rp0e9i3psPlw; lms_ads=AQGJAFOpD7Ij8gAAAX5P56_xR2RnnpHvzV7PrTt1XFYLLXOfaxm1c1IMWHrXs3fIiVy_5jZxQFCG_Pndonz85bkJkm3flnGG; lms_analytics=AQGJAFOpD7Ij8gAAAX5P56_xR2RnnpHvzV7PrTt1XFYLLXOfaxm1c1IMWHrXs3fIiVy_5jZxQFCG_Pndonz85bkJkm3flnGG; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19005%7CMCMID%7C15228333244831983722065779036496648808%7CMCAAMLH-1642622895%7C12%7CMCAAMB-1642622895%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1642025295s%7CNONE%7CvVersion%7C5.1.1%7CMCCIDH%7C1805256044; pushPermState=default; UserMatchHistory=AQLX2VHUilNAGwAAAX5P7lNyoyxI9B84M8tf13u_SiN_IALpIUauE4yazo3Yufm_9LPkgAVn5VKMyMyhVUnY--bfSKzs3qsmM5rpP8p3d5--TLfiH1L7Yyr2FR2_AMrXURSzCgljGCNQXLQWtVy-yCYWZDkMD2IUaQP3HgVRVeioZkFsv46lBt_dzTqC5klUJUnRP7ywn60Zf_rLko6RJC-roHh9Zm87U4CXLndy15uCcrxDZtWj19oTx_C0U1qlOtZfZVieqKpd3n5WXCofxwi6EUbA_NQ2y5onENU; lidc="b=TB04:s=T:r=T:a=T:p=T:g=3867:u=732:x=1:i=1642018527:t=1642019932:v=2:sig=AQHV6hl79LViOd9L81EeA8aNCM1Ux1vn"; bcookie="v=2&fea97cf7-1aaf-4164-84b4-c7d2286b72bd"; lidc="b=TB04:s=T:r=T:a=T:p=T:g=3867:u=732:x=1:i=1642018814:t=1642019932:v=2:sig=AQG-TOHFdLb9PiOMqYMs9mRF2YMb0JDF"',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Mobile Safari/537.36'
        }

        response = requests.request("GET", url, headers=headers, data=payload).status_code

        if response != 200:
            # TODO: Sent a notification to admin
            raise ValueError(f"{company} company is not verified.")
        return company