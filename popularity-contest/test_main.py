from datetime import datetime

from main import all_kanji_from_csv_strings, get_match_string

csv_example_one = '''"time_micros","c_ip","c_ip_type","c_ip_region","cs_method","cs_uri","sc_status","cs_bytes","sc_bytes","time_taken_micros","cs_host","cs_referer","cs_user_agent","s_request_id","cs_operation","cs_bucket","cs_object"
"1693206014339368","172.71.142.38","1","","GET","/v1/kanji/%E9%9B%86","200","0","277","488000","kanjiapi.dev","http://127.0.0.1:59961/","Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) QtWebEngine/6.4.3 Chrome/102.0.5005.177 Safari/537.36","ADPycduvHuLfdAtc-f-Uyl-AONU9elsqMfPUaul2F0vpty_e_YDJ67AKrjeB3_60LKULw_l50awy-M8UxjCnP4bhuWx7","GET_Object","kanjiapi.dev","v1/kanji/集"
"1693206098543049","172.70.210.203","1","","GET","/v1/kanji/%E5%85%88","404","0","0","164000","kanjiapi.dev","http://127.0.0.1:51912/","Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) QtWebEngine/6.4.3 Chrome/102.0.5005.177 Safari/537.36","ADPycdumQl2rdAAOwaNQez9Ckrf6z1og-YMJfzF2ksCJ6OXNqJ8g-z2E3j_YgVEs10OYS3Rd6B1qTU1-ccjrF-0_zDGbcA","GET_Object","kanjiapi.dev","v1/kanji/先"'''

csv_example_two = '''"time_micros","c_ip","c_ip_type","c_ip_region","cs_method","cs_uri","sc_status","cs_bytes","sc_bytes","time_taken_micros","cs_host","cs_referer","cs_user_agent","s_request_id","cs_operation","cs_bucket","cs_object"
"1693210382477156","162.158.186.55","1","","GET","/v1/kanji/%E7%8B%99","304","0","0","168000","kanjiapi.dev","http://127.0.0.1:59696/","Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) QtWebEngine/6.4.3 Chrome/102.0.5005.177 Safari/537.36","ADPycduCECW90QuUz5JwpqNPtmOpeRzr93AAOoAdTMLW3yx_z2mgqG_-NmWDZhzVSLbNh39qf8O065AGxH8lcs7KQ9f41A","GET_Object","kanjiapi.dev","v1/kanji/狙"
"1693210449669499","162.158.186.54","1","","GET","/v1/kanji/%E5%93%80","200","0","267","493000","kanjiapi.dev","http://127.0.0.1:59696/","Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) QtWebEngine/6.4.3 Chrome/102.0.5005.177 Safari/537.36","ADPycduT6csqmrX8oq8eWbrMELcLTS8L3NAlCkNWGjhn0wfgxQOdrY2mkkSk1unw0nDMFA_wEEVPlDXukdAUEVFebYyk3w","GET_Object","kanjiapi.dev","v1/kanji/哀"
"1693210493491679","162.158.186.55","1","","GET","/v1/kanji/%E6%9B%B8","304","0","0","163000","kanjiapi.dev","http://127.0.0.1:59696/","Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) QtWebEngine/6.4.3 Chrome/102.0.5005.177 Safari/537.36","ADPycdsDJNzAQEGNdEkAg-D7zF7mTNCuxEspda0gt7NYzyIdQX5olV4uo_0SNpPLdlXNLOwZHNtKnYwz04UbkHqjYFNGEw","GET_Object","kanjiapi.dev","v1/kanji/書"'''

def test_all_kanji_from_csv_strings_keeps_correct_status_codes_and_flattens():
    assert all_kanji_from_csv_strings([csv_example_one, csv_example_two]) == ['集', '狙', '哀', '書']

def test_get_match_string():
    assert get_match_string(datetime(2023, 5, 3, 7)) == '2023_05_03_07'
    assert get_match_string(datetime(2023, 11, 14, 15)) == '2023_11_14_15'
