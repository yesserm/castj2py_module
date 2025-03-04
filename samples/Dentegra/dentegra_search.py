import json
from time import sleep
import requests
def run(bot):
    bot_name = bot.bot_name
    carrier_name = bot.current_patient['carrier_name']
    primary = bot.current_patient['primary']
    todays_date = bot.todays_date
    base_pathP = bot.getvar("base_pathP")
    current_row = bot.current_row
    full_patient_name = bot.getvar("full_patient_name")
    home_load = False

    prueba = ""

    is_active = ""

    not_found = ""

    found = ""

    smart_search_on = ""

    smart_search_results = ""

    smart_search_success = ""

    smart_search_error = ""

    smart_search_patient_index = ""

    smart_search_custom_status = ""

    json_table = ""

    json_response = ""

    smart_search_patient_status = ""

    summary_visible = ""

    savepath_form = ""

    home_load = bot.scrap.wait_for_object("present","class","module-tile-label",15)
    sleep(3)

    if home_load == True:
        bot.driver.execute_script(r"""        
        Array.from(document.querySelectorAll("a")).find(b=> b.innerText.includes("Eligibility and benefits")).click()
        """)
        sleep(float(4))
        bot.driver.execute_script(r"""        
        document.getElementById('searchNewPatient').click()""")
        sleep(float(5))
        bot.scrap.click_and_wait_if_neccesary("#firstName",0,"tag")
        bot.scrap.send_key_web("","#firstName","tag","{patient_name}")
        bot.scrap.click_and_wait_if_neccesary("#lastName",0,"tag")
        bot.scrap.send_key_web("","#lastName","tag","{patient_last_name}")
        bot.scrap.click_and_wait_if_neccesary("#dob",0,"tag")
        bot.scrap.send_key_web("","#dob","tag","{patient_dob}")
        sleep(float(2))
        bot.driver.execute_script(r"""        
        document.querySelector('button[data-testid="searchButton"]').click()""")
        found = bot.scrap.wait_for_object("visible","tag","button[data-testid='eligibilityBenefitsButton']",15)
        if found:
            bot.scrap.click_and_wait_if_neccesary("button[data-testid=\"eligibilityBenefitsButton\"]",0,"tag")
            bot.scrap.wait_for_object("visible","tag","h3[data-testid='benefitsOverviewHeadingTitle']",15)
            is_active = bot.driver.execute_script(r"""            
            const patientCard = document.querySelector('.patient-card-root .patient-card-body')
            const elegibilityField = [...patientCard.querySelectorAll('.pt-staticfield')].find((field) =>
              field.innerText.includes('Eligibility'),
            )
            const elegibilityText = elegibilityField.querySelector('.pt-staticfield-text').innerText
            const isActive = elegibilityText.trim().toLowerCase().endsWith('present')
            
            return isActive ? 1 : 2
            """)
            is_active = is_active.decode()
            bot.setvar("state_parameter",is_active) 
            savepath_form = bot.driver.execute_script(r"""            const carrier_name = arguments[1];
            const primary = arguments[2];
            const todays_date = arguments[3];
            const base_pathP = arguments[4];
            const current_row = arguments[5];
            const full_patient_name = arguments[6];
                const row = current_row;
                const base_path = "base_pathP";
                const today = "todays_date".replaceAll('/','');
            
                let path = "";
                let name_file = "";
            
                if (row[row.length - 1].includes(',')){
                    let name_files = row[row.length - 1].split(',');
                    name_file = name_files.filter(item => item.includes('Eligibility_status'));
                    name_file = name_file.length !== 0 ? name_file : "";
                }else{
                    name_file = row[row.length - 1].includes('Eligibility_status') ? row[row.length - 1] : "";
                }
            
                if (name_file == "")
                    name_file = 'Eligibility_status_carrier_name_primary_full_patient_name_' + today + ".pdf";
            
                path = base_path.concat("Prints/",name_file);
                return path;""",carrier_name, primary, todays_date, base_pathP, current_row, full_patient_name)
            savepath_form = savepath_form.decode()
            bot.setvar("home_load", home_load)
            bot.setvar("prueba", prueba)
            bot.setvar("is_active", is_active)
            bot.setvar("not_found", not_found)
            bot.setvar("found", found)
            bot.setvar("smart_search_on", smart_search_on)
            bot.setvar("smart_search_results", smart_search_results)
            bot.setvar("smart_search_success", smart_search_success)
            bot.setvar("smart_search_error", smart_search_error)
            bot.setvar("smart_search_patient_index", smart_search_patient_index)
            bot.setvar("smart_search_custom_status", smart_search_custom_status)
            bot.setvar("json_table", json_table)
            bot.setvar("json_response", json_response)
            bot.setvar("smart_search_patient_status", smart_search_patient_status)
            bot.setvar("summary_visible", summary_visible)
            bot.setvar("savepath_form", savepath_form)
            bot.execute_bot(f"C:/DentalRobot/IV/Carriers/Bots/{bot_name}/Eligibility_print.py")
            bot.scrap.click_and_wait_if_neccesary("button[data-testid=\"treatmentHistoryTab\"]",0,"tag")
            sleep(float(3))
            savepath_form = bot.driver.execute_script(r"""            const carrier_name = arguments[1];
            const primary = arguments[2];
            const todays_date = arguments[3];
            const base_pathP = arguments[4];
            const current_row = arguments[5];
            const full_patient_name = arguments[6];
                const row = current_row;
                const base_path = "base_pathP";
                const today = "todays_date".replaceAll('/','');
                
                let path = "";
                let name_file = "";
                
                if (row[row.length - 1].includes(',')){
                    let name_files = row[row.length - 1].split(',');
                    name_file = name_files.filter(item => item.includes('Eligibility_status'));
                    name_file = name_file.length !== 0 ? name_file : "";
                }else{
                    name_file = row[row.length - 1].includes('Eligibility_status') ? row[row.length - 1] : "";
                }
                
                if (name_file == "")
                    name_file = 'Eligibility_status_carrier_name_primary_full_patient_name_' + today + ".pdf";
                
                path = base_path.concat("Prints/2",name_file);
                return path;
            """,carrier_name, primary, todays_date, base_pathP, current_row, full_patient_name)
            savepath_form = savepath_form.decode()
            bot.setvar("home_load", home_load)
            bot.setvar("prueba", prueba)
            bot.setvar("is_active", is_active)
            bot.setvar("not_found", not_found)
            bot.setvar("found", found)
            bot.setvar("smart_search_on", smart_search_on)
            bot.setvar("smart_search_results", smart_search_results)
            bot.setvar("smart_search_success", smart_search_success)
            bot.setvar("smart_search_error", smart_search_error)
            bot.setvar("smart_search_patient_index", smart_search_patient_index)
            bot.setvar("smart_search_custom_status", smart_search_custom_status)
            bot.setvar("json_table", json_table)
            bot.setvar("json_response", json_response)
            bot.setvar("smart_search_patient_status", smart_search_patient_status)
            bot.setvar("summary_visible", summary_visible)
            bot.setvar("savepath_form", savepath_form)
            bot.execute_bot(f"C:/DentalRobot/IV/Carriers/Bots/{bot_name}/Eligibility_print.py")
        else:
            bot.setvar("state_parameter",3) 
    else:
        bot.setvar("state_parameter",4) 

