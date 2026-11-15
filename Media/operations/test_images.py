import requests

urls = [
    "https://images.openai.com/static-rsc-4/CFnzD1QZby7fFtFaPjlJLDJLYwqznxstGCTVgBF4iOWdl-eF1QNCKfUAHtmjQvYAHkEUk8ILF8LDu3Uu8t0AOO3xAWr3qQwkLtBGNUBPngX93vnt-FL4sHh4FwA8GYxxs_s-wZlfwgpBZOFRpyXc8ueNc5hw1vHlCS4gFcdaBlA?purpose=inline",
    "https://images.openai.com/static-rsc-4/5f8HiMHKxTLh3nIAVcC2ABeZ237raUMUzok-s5vtQbDw6Pl4szqknCLIwryMuikHcOxcUlKXx8VZT-D9JfncsBbg6GxYAhhSQaThKcRKbLngeBriIMRVxTxGHpMeSr2Lc55GvwMYe5VlnVQOhGa9Bc-49Ptc_31BFp3IMUs9c4s?purpose=inline",
    "https://images.openai.com/static-rsc-4/Ex_xAr3w3ZAiwyq2Z8otwd91gaNKO3tIGrfES5iLjax1A-dNBYVkwhsGP3oydg_hM6Ev18nhdY1-lt1ySG_6-3vgN7p-g41ptoyqio5r2zWV8l7dxfw8fd6G9RM9AJMeVceeSpi-S_y41hkqm6y_lkBBd1XtNnRvCnIYcWg_KyE?purpose=inline",
    "https://images.openai.com/static-rsc-4/PdOgFdPe0Rtb7mZyDoSt4OZWKcL1z8v3AKdgEfK-iFcJ72VKR34MBAG38ap7rFW7WbP1XShmI-a2EaD8wbafGFPhjYdy21SHg4jwWCagtpNPH11HHUwzpoQppmJPKnRyiKaZO6_zSJq2y0z1Cz_zoArKJ80PdjUp0UWBEnpA0Mg?purpose=inline",
    "https://images.openai.com/static-rsc-4/dPHeuCLaX1BgSpjfzknR9HNCoTIFXd7GytkbZDqF3AMMQI7HRaUQ0p2SnfOhiFsRsdpDC62K-DfHwwAwlVgIn1Ae8LmuhAlNolVlW2uHrjzhbrYpe01IX3ET-_ip8HGIsDCB6P6Pkejo3SJ7jjK-ptM1lyas8u0SU8P2hp6vNeo?purpose=inline",
    "https://images.openai.com/static-rsc-4/tF_6xlDpD1_Pfghtx_zYkiYSElDozay6IpkJihsUlQ4GvRaCbPm3wwU-c1V68kwtyUggXLPSQ2-D06PdG0YpD1ZEGWCBpapSGP_m9CeheWUJqBdzrItDLllmKtBi9DdwgFRjI4DTfAIL12pyEq0La4-E3I-CM_vuemkKJGws7KA?purpose=inline",
    "https://images.openai.com/static-rsc-4/DYVuhzkBVzGYv7cOvKa_d9FePxZNF54wpcml9J7pkBbhJn_oNy71cR0lqWkMNNjFG8hXpK2nL51WXRedwkaL9OVKzwbC969uEZrQzM65tDHxDjjE_nUYKvQc5hN9DWohIPvabrhnUqEq8XLoFj8zrG0H_VGVPFix_reEmZLBpuk?purpose=inline",
    "https://images.openai.com/static-rsc-4/_ecvZKAmMlpHq2SUC8RETWKQ8F8W2opCFSaM2xXUrntNWY8ZuSqsUfekw854bS9PeAd44XiQEXOzof8gpAj88Oeq9NJ4DGr51nQQPwyOVv-0CFU3FsEzFC_H2Jtc66Z0fJ9UTLFVTSJkuNXMMumAuoRZesxo0ea87IPonNpigYA?purpose=inline",
    "https://images.openai.com/static-rsc-4/nGQM0xCoWCMTzsO__f71Htw-abOnTQVctN-ahlko2_-bL187c4lDdVUX9Ti2w0oeaXgnBc97-P7Hk4JoBJBTJDYFId60TH4crZGzTejFSMnumbwyefYwuOImn628TAxFYoNmXRZdNtDIw6xLmeed8sYIpP996B2KTS62BMBLLtY?purpose=inline",
    "https://images.openai.com/static-rsc-4/dU_3jU-NNt_ivp_eH-rwPvJbr3HieiYpJxu48fILdepFlgSgULTF13-YOqSvy5BvNFkrln6z4BlSxr6O_GNpd7Y20VGn_958dXKBucjIz7HoPccyuAd213z0paLM2liem3O4uAvIlT7fqbTyoMicFMQrOglvlMr_PNH837svaOs?purpose=inline"
]

headers = {'User-Agent': 'Mozilla/5.0'}
for i, url in enumerate(urls, 1):
    try:
        r = requests.get(url, headers=headers, timeout=10)
        print(f"Scene {i}: Status {r.status_code}, length {len(r.content)}")
    except Exception as e:
        print(f"Scene {i}: Failed {e}")
