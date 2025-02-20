import json
import time
def run(bot):
    patient_name = bot.current_patient['patient_name']
    patient_last_name = bot.current_patient['patient_last_name']
    plan_medicare = bot.getvar("plan_medicare")
    carrier_name = bot.current_patient['carrier_name']
    gsheet_columns = bot.gsheet_columns
    todays_date = bot.todays_date
    policyh_last_name = bot.current_patient['policyh_last_name']
    primary = bot.current_patient['primary']
    policyh_dob = bot.current_patient['policyh_dob']
    policyh_name = bot.current_patient['policyh_name']
    relationship = bot.current_patient['relationship']
    full_patient_name = bot.getvar("full_patient_name")
    patient_dob = bot.current_patient['patient_dob']
    member_id = bot.current_patient['member_id']
    other_info = bot.other_info
    sheet = bot.sheet
    clinic_name = bot.current_patient['clinic_name']
    returned_values = bot.returned_values
    bot_name = bot.bot_name
    current_row = bot.current_row
    configP = bot.configP
    procedures_not_covered = json.loads("[]")

    found_codes = json.loads("[]")

    values = json.loads("[[], []]")

    CategoryOptions = json.loads("[]")

    Options = ""

    error_title = ""

    attemps = ""

    is_plan_hmo = ""

    if "access" in configP["client_name"].lower() and "health" in configP["client_name"].lower():
        configP = bot.driver.execute_script(r"""        const current_row = arguments[1];
        const configP = arguments[2];
        let configP = configP;
        let current_row = current_row;
        net_mode = current_row[current_row.length - 2].toLowerCase();
        
        if(!net_mode.includes(configP["network_mode"].toLowerCase())){
        	if(net_mode.includes("hmo"))
              configP["network_mode"] = "OON";
          	else
              configP["network_mode"] = net_mode.toUpperCase();
        }
        
        return configP;""",current_row, configP)
        configP = configP.decode()

    returned_values = bot.driver.execute_script(r"""    const carrier_name = arguments[1];
    const gsheet_columns = arguments[2];
    const todays_date = arguments[3];
    const policyh_last_name = arguments[4];
    const current_row = arguments[5];
    const primary = arguments[6];
    const policyh_dob = arguments[7];
    const policyh_name = arguments[8];
    const relationship = arguments[9];
    const full_patient_name = arguments[10];
    const patient_dob = arguments[11];
    const member_id = arguments[12];
    const configP = arguments[13];
    const other_info = arguments[14];
    const sheet = arguments[15];
    const clinic_name = arguments[16];
    const returned_values = arguments[17];
    const bot_name = arguments[18];
    function getStringMonth(numberOfMonth) {
        var month = new Array();
        month[0] = "January";
        month[1] = "February";
        month[2] = "March";
        month[3] = "April";
        month[4] = "May";
        month[5] = "June";
        month[6] = "July";
        month[7] = "August";
        month[8] = "September";
        month[9] = "October";
        month[10] = "November";
        month[11] = "December";
        return month[numberOfMonth];
    }
    
    function calcularEdad(fecha) {
        let hoy = new Date();
        let cumpleanos = new Date(fecha);
        let edad = hoy.getFullYear() - cumpleanos.getFullYear();
        let m = hoy.getMonth() - cumpleanos.getMonth();
    
        if (m < 0 || (m === 0 && hoy.getDate() < cumpleanos.getDate())) {
            edad--;
        }
    
        return edad;
    }
    
    //general info table
    function isDate(dateStr) {
        return !isNaN(new Date(dateStr).getDate());
    }
    
    var patient_info_extract = configP["data"]["patient_info_extract"];
    var bookmarks = configP["data"]["bookmarks"];
    let other_info = other_info;
    let rv = returned_values;
    let check = "n";
    let mode =configP["network_mode"];
    let client_info=["DentalDepot","The Smilist"]
    let doctors_name =  configP["bot_name"]["doctors_name"] != undefined && configP["bot_name"]["doctors_name"] != ""
                            ? configP["bot_name"]["doctors_name"]
                        : configP["otherInformation"] != undefined 
                            ?configP["otherInformation"]["doctors_name"] != undefined && configP["otherInformation"]["doctors_name"] != ""
                                ? configP["otherInformation"]["doctors_name"]
                                :other_info.length > 0
                                    ? other_info[0]["doctors_name"] != undefined
                                        ? other_info[0]["doctors_name"] 
                                    : ""
                                : ""
                            :other_info.length > 0
                                ? other_info[0]["doctors_name"] != undefined
                                    ? other_info[0]["doctors_name"] 
                                : ""
                            : "";
    
    let tin =   configP["bot_name"]["tin"] != undefined && configP["bot_name"]["tin"] != ""
                    ? configP["bot_name"]["tin"]
                : configP["otherInformation"] != undefined 
                    ?configP["otherInformation"]["tin"] != undefined && configP["otherInformation"]["tin"] != ""
                        ? configP["otherInformation"]["tin"]
                        :other_info.length > 0
                            ? other_info[0]["tin"] != undefined
                                ? other_info[0]["tin"] 
                            : ""
                        : ""
                    :other_info.length > 0
                        ? other_info[0]["tin"] != undefined
                            ? other_info[0]["tin"] 
                        : ""
                    : "";
    
    console.log(doctors_name);
    console.log(tin);
    if(configP["bot_name"]["specific_plan_type"] != "")configP["bot_name"]["specific_plan_type"] === "INN" ? "INN":"OUT"
      }
    if(configP['clinic_name']== "Johnston Smiles"){
        let net_mode = current_row[29];
        if (net_mode.includes("OON")) mode ="OUT" 
      }
    if(configP["client_name"]== "RevenueWell"){
        let net_mode = current_row[1];
        if(net_mode.includes("OON")) 
            mode ="OUT" 
    }
    
    let is_check_patient= mode.includes("INN")? "PatientINN":"PatientOON"
    if(bookmarks.includes(is_check_patient))
        rv["bk"][is_check_patient] = check;
    
    if(patient_info_extract.includes("DoctorName") && doctors_name != "")
        rv["bk"]["DoctorName"] = doctors_name;
    
    if(patient_info_extract.includes("TIN") && tin != "")
        rv["bk"]["TIN"] = tin;
    
    if(patient_info_extract.includes("InNetwork") && configP["client_name"] != "Peak Dental Services")
        rv["bk"][mode == "INN" ? "InNetworkYES" : "InNetworkNO"] = check;
    
    if(patient_info_extract.includes("Relationshipto"))relationship".toLowerCase().trim() == "child" || "relationship".toLowerCase().trim() == "dependent"){
            rv["bk"]["RelationshiptoDependent"] = check;
        }else if("relationship".toLowerCase().trim() == "self"){
            rv["bk"]["RelationshiptoSelf"] = check;
        }else if("relationship".toLowerCase().trim() == "spouse"){
            rv["bk"]["RelationshiptoSpouse"] = check;
        }else
            rv["bk"]["RelationshiptoOther"] = check;
    }
    console.log(rv)
    if(patient_info_extract.includes("CoverageType"))relationship".toLowerCase().trim() == "self")
            rv["bk"]["CoverageTypeSingle"] = check;
        else
            rv["bk"]["CoverageTypeFamily"] = check;
    }
    
    if(patient_info_extract.includes("Paymentbasedon") && !bookmarks.includes("PaymentbasedonPrepDate"))configP["network_mode"] == "INN")
            rv["bk"]["PaymentbasedonFeeSchedule"] = check;
        else
            rv["bk"]["PaymentbasedonUCR"] = check;
    }
    
    if(patient_info_extract.includes("OfficeName"))
        rv["bk"]["OfficeName"] = "clinic_name";
    
    if(patient_info_extract.includes("AppointmentDate")){
        let date_app="sheet";
        date_app = date_app.split("-")[1] + "/" + date_app.split("-")[2]+ "/" + date_app.split("-")[0];
        rv["bk"]["AppointmentDate"] = date_app;
    }
    
    if(patient_info_extract.includes("PrimaryPolicyholderName"))
        rv["bk"]["PrimaryPolicyholderName"] = "policyh_name" + " " + "policyh_last_name";
    
    if(patient_info_extract.includes("PatientName") && ![client_info].includes(configP["client_name"]))
        rv["bk"]["PatientName"] = "full_patient_name";
    
    if(patient_info_extract.includes("InsuranceName"))
        rv["bk"]["InsuranceName"] = "carrier_name";
    
    if(patient_info_extract.includes("DUP_InsuranceName"))
        rv["bk"]["DUP_InsuranceName"] = "carrier_name";
    
    if(patient_info_extract.includes("PatientRelationtoSuscriber"))
        rv["bk"]["PatientRelationtoSuscriber"] = "relationship";
    
    if(patient_info_extract.includes("PatientDOB"))
        rv["bk"]["PatientDOB"] = "patient_dob";
    
    if(patient_info_extract.includes("MemberID") && configP["client_name"] !="Go Dental")
        rv["bk"]["MemberID"] = "member_id";
    
    if(patient_info_extract.includes("PrimaryPolicyholderMemberID"))
        rv["bk"]["PrimaryPolicyholderMemberID"] = "member_id";
    
    if(patient_info_extract.includes("PrimaryPolicyholderDOB"))
        rv["bk"]["PrimaryPolicyholderDOB"] = "policyh_dob";
    
    if(patient_info_extract.includes("VerificationDoneBy"))
        rv["bk"]["VerificationDoneBy"] = "DentalRobot";
    
    if(patient_info_extract.includes("Date"))
        rv["bk"]["Date"] = "todays_date";
    
    if(patient_info_extract.includes("PayerID"))
        rv["bk"]["PayerID"] = "60054";
    
    if(patient_info_extract.includes("DUP_PayerID"))
        rv["bk"]["DUP_PayerID"] = "60054";
    
    if(patient_info_extract.includes("State"))configP['client_name']== 'Smile Design' ? 'KY':'Kentucky'
        rv["bk"]["State"] = state;
    }
    
    if(patient_info_extract.includes("GroupID") && configP["client_name"] === "Barbaro"){
        let columns = gsheet_columns;
        let row = current_row;
        let index_group = columns[0].findIndex(i => i.includes('Group Number'));
    
        let group_number = index_group !== -1 ? row[index_group] : "-";
    
        rv["bk"]["GroupID"] = group_number;
    }
    
    if(patient_info_extract.includes("ZIP"))configP['client_name']== 'Smile Design' ? '40512':"14094";
        rv["bk"]["ZIP"] = zip;
    }
    
    if(patient_info_extract.includes("CallReference"))
        rv["bk"]["CallReference"] = "(800) 451-7715";
    
    if(patient_info_extract.includes("DUP_CallReference"))
        rv["bk"]["DUP_CallReference"] = "(800) 451-7715";
    
    if(patient_info_extract.includes("TOA"))
        rv["bk"]["TOANO"] = check;
    
    if(patient_info_extract.includes("PaymentbasedonFeeSchedule") && !bookmarks.includes("PaymentbasedonPrepDate"))
        rv["bk"]["PaymentbasedonFeeScheduleYES"] = check;
    
    if(patient_info_extract.includes("Verification"))
        rv["bk"]["VerificationDoneByONLINE"] = check;
    
    if(patient_info_extract.includes("PlanUse"))
        rv["bk"]["PlanUsePatientID"] = check;
    
    if(patient_info_extract.includes("Insurancecoverage"))
        rv["bk"]["primary".toLowerCase() == "primary" ? "InsurancecoveragePRIMARY" : "InsurancecoverageSECONDARY"] = check;
    if(patient_info_extract.includes("Insurancecoverage"))
        rv["bk"]["primary".toLowerCase() == "primary" ? "InsurancecoveragePRIMARY" : "InsurancecoverageSECONDARY"] = check;
    if(patient_info_extract.includes("Time")){
        let time = new Date().toLocaleString('en-US', { hour: 'numeric', minute:'numeric',hour12: true });
        rv["bk"]["Time"] = time;
    }
    if(configP['client_name'== "Heartland"] || configP["client_name"]== "Salt Dental Partners")primary".toLowerCase() == "primary" ? "PlanPRIMARY" : "PlanSECONDARY"] = check;
    }
    if(patient_info_extract.includes("Patientage")){
        let age = calcularEdad("patient_dob");
    
        if(age > 0)
            rv["bk"]["Patientage"] = age;
    }
    
    
    
    if(patient_info_extract.includes("Copay"))
        rv["bk"]["CopayNO"] = check;
    
    if(patient_info_extract.includes("Crownspaidon"))
        rv["bk"]["CrownspaidonSEAT"] = check;
    if(patient_info_extract.includes("Website"))
        rv["bk"]["Website"] = "https://www.aetna.com/";
    if(patient_info_extract.includes("Active"))
        rv["bk"]["ActiveYES"] = check
    if(patient_info_extract.includes("IsthereanywaitingPeriodNO"))
        rv["bk"]["IsthereanywaitingPeriodNO"] = check
    return rv;""",carrier_name, gsheet_columns, todays_date, policyh_last_name, current_row, primary, policyh_dob, policyh_name, relationship, full_patient_name, patient_dob, member_id, configP, other_info, sheet, clinic_name, returned_values, bot_name)

    returned_values = returned_values.decode()

    if insurance:
        if configP["client_name"] == "DentalDepot":
            is_plan_hmo = bot.driver.execute_script(r"""            const configP = arguments[1];
            var inner_tables = document.querySelectorAll('.table-inner')
            let configP = configP;
            let is_hmo_plan = "INN"
            if (inner_tables.length > 0) {
                let payer_tbl = Array.from(inner_tables).find(i => i.innerText.toUpperCase().includes("PLAN TYPE"));
                let dates_tbl = Array.from(inner_tables).find(i => i.innerText.toUpperCase().includes("ELIGIBILITY BEGIN"));
                if (typeof payer_tbl !== "undefined") {
                    let plan_type_index = payer_tbl.querySelectorAll('td')[0].innerText.split("
            ").findIndex(i => i.toUpperCase().includes("PLAN TYPE"));
                    if (plan_type_index !== -1) {
                        let plan_type = payer_tbl.querySelectorAll('td')[1].innerText.split("
            ")[plan_type_index];
                        console.log(plan_type)
                      	if(plan_type.toUpperCase().includes("HMO")){
                          is_hmo_plan = "OON"
                        }
                    }
                }
            }
            return is_hmo_plan""",configP)
            is_plan_hmo = is_plan_hmo.decode()
        returned_values = bot.driver.execute_script(r"""        const current_row = arguments[1];
        const is_plan_hmo = arguments[2];
        const patient_name = arguments[3];
        const configP = arguments[4];
        const patient_last_name = arguments[5];
        const returned_values = arguments[6];
        const bot_name = arguments[7];
        const plan_medicare = arguments[8];
        function extractEndDate(date) {
          if (date != "") {
              if (date.match(/01\/01/gi) != null)
                  return "12/31/" + new Date().getFullYear();
              else {
                  let e = new Date(date);
                  e.setMonth(e.getMonth() +12);
                  e.setDate(0);
                  return (e.getMonth() + 1) + "/"+e.getDate()+"/"+  (e.getFullYear());
              }
          } else
              return date;
        }
        
        function isEndDateBeforeToday(endDate) {
          let today = new Date();
          let endDateObj = new Date(endDate);
          return endDateObj > today;
        }
        
        function getStringMonth(numberOfMonth) {
          let month = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
          return month[numberOfMonth];
        }
        
        const formatter = new Intl.NumberFormat('en-US', {
          style: 'currency',
          currency: 'USD',
          minimumFractionDigits: 2
        });
        //let rv= }
        let rv = returned_values;
        let patient_info_extract = configP["data"]["patient_info_extract"];
        let bookmarks = configP["data"]["bookmarks"];
        let client_info = ["DentalDepot","The Smilist"];
        let clinic_onn=["clinic#vigp","Southern Pines Smiles"]
        let check = "n";
        let mode = "IN";
        
        if (configP["network_mode"] == "OON") 
          mode = "OUT";
        
        
        if ((configP["client_name"] == "Ruby Canyon Dental" || clinic_onn.includes(configP["clinic_name"]))&& configP["bot_name"]["specific_plan_type"] != '')
          mode = configP["bot_name"]["specific_plan_type"] == "OON" ? "OUT" : "INN";
        if(configP["bot_name"]["specific_plan_type"] != "")configP["bot_name"]["specific_plan_type"] === "INN" ? "IN":"OUT OF"
        }
        if(configP["client_name"]== "RevenueWell")current_row[1];
          if (net_mode.includes("OON")) mode ="OUT" 
        }
        if(configP['clinic_name']== "Johnston Smiles")current_row[29];
          if (net_mode.includes("OON")) mode ="OUT" 
        }
        
        if(configP["client_name"]== "DentalDepot"){
          let is_plan_hmo = "is_plan_hmo";
          if (is_plan_hmo.includes("OON") && "plan_medicare" === "False") mode ="OUT"
        
          
        }
        //console.info(mode)
        //Get Genral Information
        let plan_type = Array.from(document.querySelectorAll(".table-inner")).find(table => table?.innerText.toUpperCase().includes("PLAN TYPE"));
        plan_type = plan_type != undefined ? plan_type.querySelectorAll("td") : undefined;
        plan_type = plan_type != undefined ? plan_type[1].innerText.split("
        ")[plan_type[0].innerText.split("
        ").findIndex(row => row.toUpperCase().includes("PLAN TYPE"))] : undefined;
        plan_type = plan_type != undefined ? plan_type : "";
        
        
        let description = Array.from(document.querySelectorAll(".table-inner")).find(table => table?.innerText.toUpperCase().includes("DESCRIPTION"));
        description = description != undefined ? description.querySelectorAll("td") : undefined;
        description = description != undefined ? description[1].innerText.split("
        ")[description[0].innerText.split("
        ").findIndex(row => row.toUpperCase().includes("DESCRIPTION"))] : undefined;
        description = description != undefined ? description : "";
        
        let coverage = Array.from(document.querySelectorAll(".table-inner")).find(table => table?.innerText.toUpperCase().includes("COVERAGE"));
        coverage = coverage != undefined ? coverage.querySelectorAll("td") : undefined;
        coverage = coverage != undefined ? coverage[1].innerText.split("
        ")[coverage[0].innerText.split("
        ").findIndex(row => row.toUpperCase().includes("COVERAGE"))] : undefined;
        coverage = coverage != undefined ? coverage : "";
        
        let effectivedate = Array.from(document.querySelectorAll(".table-inner")).find(table => table?.innerText.toUpperCase().includes("PLAN BEGIN"));
        effectivedate = effectivedate != undefined ? effectivedate.querySelectorAll("td") : undefined;
        effectivedate = effectivedate != undefined ? effectivedate[1].innerText.split("
        ")[effectivedate[0].innerText.split("
        ").findIndex(row => row.toUpperCase().includes("PLAN BEGIN"))] : undefined;
        effectivedate = effectivedate != undefined ? effectivedate : "";
        
        let name = Array.from(document.querySelectorAll(".table-inner")).find(table => table?.innerText.toUpperCase().includes("NAME:"));
        name = name != undefined ? name.querySelectorAll("td") : undefined;
        name = name != undefined ? name[1].innerText.split("
        ")[name[0].innerText.split("
        ").findIndex(row => row.toUpperCase().includes("NAME:"))] : undefined;
        name = name != undefined ? name : "";
        
        if(patient_info_extract.includes("InNetworkPlan") && plan_type != "")
        rv["bk"]["InNetworkPlan"] = plan_type;
        
        if (patient_info_extract.includes("InNetworkplan") && plan_type != "" && !bookmarks.includes("InNetworkYES"))
        rv["bk"]["InNetworkplan"] = plan_type;
        
        if (patient_info_extract.includes("InNetwork") && plan_type != "" && !bookmarks.includes("InNetworkYES"))
        rv["bk"]["InNetwork"] = plan_type;
        
        if(patient_info_extract.includes("InNetwork") && configP["client_name"] == "Peak Dental Services")
        rv["bk"][((plan_type.toLowerCase().includes("ppo") || plan_type.toLowerCase().includes("hmo") ) ? "InNetworkYES" : "InNetworkNO")] = check;
        
        if(patient_info_extract.includes("FeeScheduleName") && plan_type != "")
        rv["bk"]["FeeScheduleName"] = plan_type;
        
        if(patient_info_extract.includes("productName") && plan_type != "" && description != "")
        rv["bk"]["productName"] = `${plan_type}, ${description}`;
        
        if(patient_info_extract.includes("Paymentbasedon") && !bookmarks.includes("PaymentbasedonPrepDate"))
        rv["bk"][((plan_type != "") ? "PaymentbasedonFeeScheduleYES" : "PaymentbasedonFeeScheduleNO")] = check;
        
        /*if (patient_info_extract.includes("CoverageType") && coverage != ""){
        if (coverage.includes("Family") || coverage.includes("Employee and Children"))
          rv["bk"]["CoverageTypeFamily"] = check;
        else
          rv["bk"]["CoverageTypeSingle"] = check;
        }*/
        
        if (patient_info_extract.includes("EffectiveDate") && effectivedate != "")
        rv["bk"]["EffectiveDate"] = effectivedate;
        
        if(client_info.includes(configP["client_name"]) && patient_info_extract.includes("PatientName"))
        rv["bk"]["PatientName"] = name != "" ? name : "patient_name" + " " + "patient_last_name";
        
        let provider_table = Array.from(document.querySelectorAll(".providerTable tbody tr"))|| [];
        let address_index = provider_table.findIndex(item => item.innerText.includes("Address:"));
        let address_info = "";
        //console.log(address_index)
        if(address_index != -1){
          if (address_index !== -1) {
              address_info = provider_table.slice(address_index, address_index + 2)
                  .map(item => item.querySelectorAll("td")[1]?.innerText.trim() || "")
                  .filter(text => text !== "");
          }
          address_info =address_info.join(",")
          //console.warn(address_info)
        }
        
        if (address_info != "" && address_index != -1){
            let street = address_info.match(/P(.)?O(.)? Box \d1,/gi);
            street = street != null ? street[0] : "";
            
            let city = address_info.replace(/(P(.)?O(.)? Box \d1,|,)/gi, "");
            city = city?.trim().split(" ")[0];
            
            let state = address_info.replace(/(P(.)?O(.)? Box \d1,|,)/gi, "");
            state = state?.trim().split(" ")[1];
            
            let zip = address_info.replace(/(P(.)?O(.)? Box \d1,|,)/gi, "");
        
            zip = zip?.trim().split(" ")[2]; 
            //console.warn({address_info,street,city,state,zip})
            if(patient_info_extract.includes("ClaimsAddress"))
              rv["bk"]["ClaimsAddress"] = address_info;
            
            if(patient_info_extract.includes("DUP_ClaimsAddress"))
              rv["bk"]["DUP_ClaimsAddress"] = address_info;
            
            if(patient_info_extract.includes("Street"))
              rv["bk"]["Street"] = street;
            
            if(patient_info_extract.includes("City"))
              rv["bk"]["City"] = city;
            if(patient_info_extract.includes("ZIP"))
              rv["bk"]["ZIP"] = zip;
            if(patient_info_extract.includes("State"))
              rv["bk"]["State"] = state;
        }else{
            if(patient_info_extract.includes("State")){
                let state = configP['client_name']== 'Smile Design' ? 'KY':'Kentucky'
                rv["bk"]["State"] = state;
            }
            if(patient_info_extract.includes("ZIP"))configP['client_name']== 'Smile Design' ? '40512':"14094";
              rv["bk"]["ZIP"] = zip;
            }
            if(patient_info_extract.includes("ClaimsAddress"))
              rv["bk"]["ClaimsAddress"] = "Aetna Dental P.O. Box 14094 Lexington, KY 40512";
        
            if(patient_info_extract.includes("DUP_ClaimsAddress"))
              rv["bk"]["DUP_ClaimsAddress"] = "P.O. Box 14094";
        
            if(patient_info_extract.includes("Street"))
              rv["bk"]["Street"] = "P.O. Box 14094";
        
            if(patient_info_extract.includes("City"))
              rv["bk"]["City"] = "Lexington";
        }
        
        let exist_benefit_OON = Array.from(document.querySelectorAll("legend")).map(item => item?.innerText).some(item => item.includes("Service Level Benefits") && item.toUpperCase().includes("OUT OF NETWORK")); 
        
        if (patient_info_extract.includes("OutofNetwork"))
        rv["bk"][((exist_benefit_OON == true) ? "OutofNetworkYES" : "OutofNetworkNO")] = check;
        if (patient_info_extract.includes("OON_Pay"))
        rv["bk"][((exist_benefit_OON == true)? "OON_PayYES":"OON_PayNO")] = check;
        
        if (patient_info_extract.includes("DoesthisplanofferOONBenefits"))
        rv["bk"][((exist_benefit_OON == true) ? "DoesthisplanofferOONBenefitsYES" : "DoesthisplanofferOONBenefitsNO")] = check;
        
        let memberID = Array.from(document.querySelectorAll(".table-inner")).find(table => table?.innerText.toUpperCase().includes("MEMBER ID"));
        memberID = memberID != undefined ? memberID.querySelectorAll("td") : undefined;
        memberID = memberID != undefined ? memberID[1].innerText.split("
        ")[memberID[0].innerText.split("
        ").findIndex(row => row.toUpperCase().includes("MEMBER ID"))] : undefined;
        memberID = memberID != undefined ? memberID : "";
        
        if (patient_info_extract.includes("MemberID") && memberID != "" && configP["client_name"] == "Go Dental")
        rv["bk"]["MemberID"] = memberID;
        
        let group_number = Array.from(document.querySelectorAll(".table-inner")).find(table => table?.innerText.toUpperCase().includes("GROUP#"));
        group_number = group_number != undefined ? group_number.querySelectorAll("td") : undefined;
        group_number = group_number != undefined ? group_number[1].innerText.split("
        ")[group_number[0].innerText.split("
        ").findIndex(row => row.toUpperCase().includes("GROUP#"))] : undefined;
        group_number = group_number != undefined ? group_number : "";
        
        let plan_number = Array.from(document.querySelectorAll(".table-inner")).find(table => table?.innerText.toUpperCase().includes("PLAN#"));
        plan_number = plan_number != undefined ? plan_number.querySelectorAll("td") : undefined;
        plan_number = plan_number != undefined ? plan_number[1].innerText.split("
        ")[plan_number[0].innerText.split("
        ").findIndex(row => row.toUpperCase().includes("PLAN#"))] : undefined;
        plan_number = plan_number != undefined ? plan_number : "";
        
        let group_name = Array.from(document.querySelectorAll(".table-inner")).find(table => table?.innerText.toUpperCase().includes("GROUP NAME"));
        group_name = group_name != undefined ? group_name.querySelectorAll("td") : undefined;
        group_name = group_name != undefined ? group_name[1].innerText.split("
        ")[group_name[0].innerText.split("
        ").findIndex(row => row.toUpperCase().includes("GROUP NAME"))] : undefined;
        group_name = group_name != undefined ? group_name : "";
        
        let group_number_valid = group_number;
        let group_name_number = "";
        
        if (patient_info_extract.includes("GroupName") && group_name != "")
        rv["bk"]["GroupName"] = group_name;
        
        if (patient_info_extract.includes("DUP_GroupName") && group_name != "")
        rv["bk"]["DUP_GroupName"] = group_name;
        
        if (patient_info_extract.includes("Employer") && group_name != "")
        rv["bk"]["Employer"] = group_name;
        
        let not_client_group_id = ["Access Health Dental","Barbaro","The Smilist"]
        if (!not_client_group_id.includes(configP["client_name"])) {
          if (patient_info_extract.includes("GroupID") && group_number != "")
            rv["bk"]["GroupID"] = group_number;
        
          if (patient_info_extract.includes("DUP_GroupID") && group_number != "")
            rv["bk"]["DUP_GroupID"] = group_number;
        
          group_number_valid = group_number;
        }
        
        let client_plan_number = ["Access Health Dental","The Smilist","Salt Dental Partners"]
        if (client_plan_number.includes(configP["client_name"])) {
          if (patient_info_extract.includes("GroupID") && plan_number != "")
            rv["bk"]["GroupID"] = plan_number;
        
          if (patient_info_extract.includes("DUP_GroupID") && plan_number != "")
            rv["bk"]["DUP_GroupID"] = plan_number;
        
          if (patient_info_extract.includes("PlanID") && plan_number != "")
            rv["bk"]["PlanID"] = plan_number;
        
        
          group_number_valid = plan_number;
        }
        
        if (patient_info_extract.includes("PatientSex") && rv?.Gender) {
          rv['bk']['PatientSex'] = rv.Gender
        }
        
        if(group_number_valid != "" && group_name != "")
        group_name_number = group_number_valid + " // " + group_name;
        else if(group_number_valid != "")
        group_name_number = group_number_valid;
        else if(group_name != "")
        group_name_number = group_name;
        
        if (patient_info_extract.includes("GroupNameAndGroupID") && group_name_number != "")
        rv["bk"]["GroupNameAndGroupID"] = group_name_number;
        
        let network_type = Array.from(document.querySelectorAll(".table-inner")).find(table => table?.innerText.toUpperCase().includes("NETWORK TYPE"));
        network_type = network_type != undefined ? network_type.querySelectorAll("td") : undefined;
        network_type = network_type != undefined ? network_type[1].innerText.split("
        ")[network_type[0].innerText.split("
        ").findIndex(row => row.toUpperCase().includes("NETWORK TYPE"))] : undefined;
        network_type = network_type != undefined ? network_type : "";
        
        if (patient_info_extract.includes("Coordinationofbenefits") && network_type != ""){
        if (network_type.toUpperCase().includes("STANDARD DENTAL NETWORK"))
          rv["bk"]["CoordinationofbenefitsSTANDARD"] = check;
        else if (network_type.toUpperCase().includes("DUPLICATING")) 
          rv["bk"]["CoordinationofbenefitsNONDuplicating"] = check;
        }
        
        if (patient_info_extract.includes("COB") && network_type != "") {
        if (network_type.toUpperCase().includes("STANDARD DENTAL NETWORK"))
          rv["bk"]["CoordinateBenefitsYES"] = check;
        else if (network_type.toUpperCase().includes("DUPLICATING"))
          rv["bk"]["CoordinateBenefitsNO"] = check;
        }
        
        if (patient_info_extract.includes("CoordinateBenefits") && network_type != ""){
        if (network_type.toUpperCase().includes("STANDARD DENTAL NETWORK"))
          rv["bk"]["CoordinateBenefitsYES"] = check;
        else if (network_type.toUpperCase().includes("DUPLICATING"))
          rv["bk"]["CoordinateBenefitsNO"] = check;
        }
        
        if (patient_info_extract.includes("CoordinationofBenefitsCOB") && network_type != "") {
        if (network_type.toUpperCase().includes("STANDARD DENTAL NETWORK"))
          rv["bk"]["CoordinationofBenefitsCOB"] = "Standard";
        else if (network_type.toUpperCase().includes("DUPLICATING"))
          rv["bk"]["CoordinationofBenefitsCOB"] = "Duplicating";
        else
          rv["bk"]["CoordinationofBenefitsCOB"] = network_type.split(",")[0];
        }
        
        if(patient_info_extract.includes("Month") && effectivedate != "") {
        let date = effectivedate.split("/")[0];
        let month = getStringMonth(parseInt(date) - 1);
          rv["bk"]["Month"] = month;
        }
        
        
        let plan_level_remarks = Array.from(document.querySelectorAll(".well")).find(panel => panel.querySelector("legend")?.innerText.toUpperCase().includes("PLAN LEVEL REMARKS"));
        let notes = plan_level_remarks != undefined ? Array.from(plan_level_remarks.querySelectorAll("tr:not(.headers)")).filter(item => item?.innerText.trim() != "") : [];
        
        if (patient_info_extract.includes("StudentAge") && notes.some(note => note?.innerText.includes("STUDENT")))
          rv["bk"]["StudentAge"] = notes.find(note => note?.innerText.includes("STUDENT"))?.innerText.match(/\d1,2/g)[1];
        
        if (patient_info_extract.includes("MissingToothClause")){
        if(notes.some(note => note?.innerText.includes("MISSING TOOTH CLAUSE APPLIES")))
          rv["bk"]["MissingToothClauseYES"] = check;
        else
          rv["bk"]["MissingToothClauseNO"] = check;
        }
        // console.error(mode)
        //Get Deductibles information ------------------------------------------------------------------------------------------------------------
        let table_maximums = Array.from(document.querySelectorAll(".well")).find(panel => panel.querySelector("legend")?.innerText.toUpperCase().includes(mode) && panel.querySelector("legend")?.innerText.toUpperCase().includes("MAXIMUMS"));
        headers = table_maximums != undefined ? Array.from(table_maximums.querySelectorAll("th")).filter(item => item?.innerText.trim() != "") : [];
        rows = table_maximums != undefined ? Array.from(table_maximums.querySelectorAll("tr:not(.headers)")).filter(item => item?.innerText.trim() != "") : [];
        
        let table_maximums_lifetime = Array.from(document.querySelectorAll(".well")).find(panel => panel.querySelector("legend")?.innerText.toUpperCase().includes(mode) && panel.querySelector("legend")?.innerText.toUpperCase().includes("MAXIMUMS"));
        headers_ortho = table_maximums_lifetime != undefined ? Array.from(table_maximums.querySelectorAll("th")).filter(item => item?.innerText.trim() != "") : [];
        rows_ortho = table_maximums_lifetime != undefined ? Array.from(table_maximums.querySelectorAll("tr:not(.headers)")).filter(item => item?.innerText.trim() != "") : [];
        console.log(table_maximums,"lifetime")
        
        let table_deductible = Array.from(document.querySelectorAll(".well")).find(panel => panel.querySelector("legend")?.innerText.toUpperCase().includes(mode) && panel.querySelector("legend")?.innerText.toUpperCase().includes("DEDUCTIBLES"));
        headers_ded = table_deductible != undefined ? Array.from(table_deductible.querySelectorAll("th")).filter(item => item?.innerText.trim() != "") : [];
        rows_ded = table_deductible != undefined ? Array.from(table_deductible.querySelectorAll("tr:not(.headers)")).filter(item => item?.innerText.trim() != "") : [];
        //console.error(table_deductible)
        //console.info(mode)
        let table_deductible_ortho = Array.from(document.querySelectorAll(".well")).find(panel => panel.querySelector("legend")?.innerText.toUpperCase().includes(mode) && panel.querySelector("legend")?.innerText.toUpperCase().includes("DEDUCTIBLES"));
        headers_ded_ortho = table_deductible_ortho != undefined ? Array.from(table_deductible_ortho.querySelectorAll("th")).filter(item => item?.innerText.trim() != "") : [];
        rows_ded_ortho = table_deductible_ortho != undefined ? Array.from(table_deductible_ortho.querySelectorAll("tr:not(.headers)")).filter(item => item?.innerText.trim() != "") : [];
        
        //console.info(headers_ded_ortho)
        let index_type = headers_ded.findIndex(item => item?.innerText.toUpperCase().includes("TYPE"));
        let index_coverage = headers_ded.findIndex(item => item?.innerText.toUpperCase().includes("COVERAGE"));
        let index_amount = headers_ded.findIndex(item => item?.innerText.toUpperCase().includes("AMOUNT"));
        let index_remaining = headers_ded.findIndex(item => item?.innerText.toUpperCase().includes("REMAINING"));
        
        let deduc = "";
        let rem_deduc = "";
        let used_deduc = "";
        
        let deduc_ortho = "";
        let rem_deduc_ortho = "";
        let used_deduc_ortho = "";
        
        let fam_deduc = "";
        let fam_rem_deduc = "";
        let fam_used_deduc = "";
        
        let index_type_deduc_ortho = headers_ded_ortho.findIndex(item => item?.innerText.toUpperCase().includes("TYPE"));
        let index_coverage_deduc_ortho = headers_ded_ortho.findIndex(item => item?.innerText.toUpperCase().includes("COVERAGE"));
        let index_amount_deduc_ortho = headers_ded_ortho.findIndex(item => item?.innerText.toUpperCase().includes("AMOUNT"));
        let index_remaining_deduc_ortho = headers_ded_ortho.findIndex(item => item?.innerText.toUpperCase().includes("REMAINING"));
        //console.error(index_coverage_deduc_ortho)
        if(index_coverage_deduc_ortho != -1){
          rows_ded_ortho = rows_ded_ortho.find(row => row.querySelectorAll("td")[index_coverage]?.innerText.includes("Individual") && 
          row.querySelectorAll("td")[index_type]?.innerText.includes("Ortho"));
          //console.log(rows_ded_ortho)
          if(rows_ded_ortho === undefined){
              table_deductible_ortho = Array.from(document.querySelectorAll(".well")).find(panel => panel.querySelector("legend")?.innerText.includes("Deductibles - In and Out of Network"))
              console.log(table_deductible_ortho,"orsh")
              rows_ded_ortho = table_deductible_ortho != undefined ? Array.from(table_deductible_ortho.querySelectorAll("tr:not(.headers)")).filter(item => item?.innerText.trim() != "") : [];
              rows_ded_ortho = rows_ded_ortho.find(row => row.querySelectorAll("td")[index_coverage_deduc_ortho]?.innerText.includes("Individual") && row.querySelectorAll("td")[index_type_deduc_ortho]?.innerText.includes("Ortho"));
              console.warn(rows_ded_ortho)
              if(index_amount_deduc_ortho != -1 && rows_ded_ortho != undefined){
                  deduc_ortho = rows_ded_ortho != undefined ? rows_ded_ortho.querySelectorAll("td")[index_amount_deduc_ortho]?.innerText.trim() : undefined;
                  //console.log(deduc_ortho)
                  if (patient_info_extract.includes("Orthodontics_Deductible") && deduc_ortho != undefined)
                    rv["bk"]["Orthodontics_Deductible"] = deduc_ortho;
                
              }        
          }
        }
        
        if(index_coverage != -1){
        let row_ded = rows_ded.find(row => row.querySelectorAll("td")[index_coverage]?.innerText.includes("Individual") && 
                                            !row.querySelectorAll("td")[index_type]?.innerText.includes("Ortho"));
        
        if(index_amount != -1 && rows_ded != undefined) {
          deduc = row_ded != undefined ? row_ded.querySelectorAll("td")[index_amount]?.innerText.trim() : undefined;
        
          if (patient_info_extract.includes("Deductible") && deduc != undefined)
            rv["bk"]["Deductible"] = deduc;
        }
        
        if(index_remaining != -1 && rows_ded != undefined) {
          rem_deduc = row_ded != undefined ? row_ded.querySelectorAll("td")[index_remaining]?.innerText.trim() : undefined;
        
          if (patient_info_extract.includes("RemainingDeductible") && rem_deduc != undefined)
            rv["bk"]["RemainingDeductible"] = rem_deduc;
        }
        
        if(rem_deduc != undefined && deduc != undefined && rows_ded != undefined){
          used_deduc = formatter.format(parseFloat(deduc.replace(/(\$|,)/g, "")) - parseFloat(rem_deduc.replace(/(\$|,)/g, ""))); 
          
          if (patient_info_extract.includes("DeductibleAmountUsedtoDate")) 
            rv["bk"]["DeductibleAmountUsedtoDate"] = used_deduc;
        
          if (patient_info_extract.includes("Deductible_Used"))
            rv["bk"]["Deductible_Used"] = used_deduc;
        
          if (patient_info_extract.includes("Met_Deductible"))
            rv["bk"]["Met_Deductible"] = used_deduc;
        
          if (patient_info_extract.includes("DeductibleMet")){
            let rem_val = parseFloat(rem_deduc.replace(/(\$|,)/g, ""));
            let deduc_val = parseFloat(deduc.replace(/(\$|,)/g, ""));
            if (deduc_val > 0 ) {
              let bk_met_deductible = rem_val <= 0 ? "DeductibleMetYES" : "DeductibleMetNO"
              rv["bk"][bk_met_deductible] = check;
            }
          }
        }
        
        row_ded = rows_ded.find(row => row.querySelectorAll("td")[index_coverage]?.innerText.includes("Family") && 
                                        !row.querySelectorAll("td")[index_type]?.innerText.includes("Ortho"));
        
        if(index_amount != -1 && rows_ded != undefined) {
          fam_deduc = row_ded != undefined ? row_ded.querySelectorAll("td")[index_amount]?.innerText.trim() : undefined;
        
          if (patient_info_extract.includes("Family") && fam_deduc != undefined)
            rv["bk"]["Family"] = fam_deduc ;
        }
        
        if(index_remaining != -1 && rows_ded != undefined) {
          fam_rem_deduc = row_ded != undefined ? row_ded.querySelectorAll("td")[index_remaining]?.innerText.trim() : undefined;
        
          if (patient_info_extract.includes("Remaining_FamilyDeductible") && fam_rem_deduc != undefined)
            rv["bk"]["Remaining_FamilyDeductible"] = fam_rem_deduc;
        }
        
        if(fam_rem_deduc != undefined && fam_deduc != undefined && rows_ded != undefined){
          fam_used_deduc = formatter.format(parseFloat(fam_deduc.replace(/(\$|,)/g, "")) - parseFloat(fam_rem_deduc.replace(/(\$|,)/g, ""))); 
          
          if (patient_info_extract.includes("Met_Family"))
            rv["bk"]["Met_Family"] = fam_used_deduc;
          if (patient_info_extract.includes("AmountFamilyUsedToDate"))
            rv["bk"]["AmountFamilyUsedToDate"] = fam_used_deduc;
          if (patient_info_extract.includes("DeductibleFamMet") ) {
            let fam_rem_val = parseFloat(fam_rem_deduc.replace(/($|,)/, ""));
            let ded_fam_bk = fam_rem_val > 0 ? "DeductibleFamMetNO" :"DeductibleFamMetYES"
            rv["bk"][ded_fam_bk] = check;
          }
        }
        
        
        }
        
        index_type = headers.findIndex(item => item?.innerText.toUpperCase().includes("TYPE"));
        index_coverage = headers.findIndex(item => item?.innerText.toUpperCase().includes("COVERAGE"));
        index_amount = headers.findIndex(item => item?.innerText.toUpperCase().includes("AMOUNT"));
        index_remaining = headers.findIndex(item => item?.innerText.toUpperCase().includes("REMAINING"));
        let index_message_max  = headers.findIndex(item => item?.innerText.toUpperCase().includes("MESSAGE"))
        //console.log(index_coverage)
        let max = "";
        let rem = "";
        let used = "";
        
        let fam_max = "";
        let fam_rem = "";
        let fam_used = "";
        
        let ortho_max = "";
        let ortho_rem = "";
        let ortho_used = "";
        if(index_message_max != -1){
        let row_max = rows.find(row => row.querySelectorAll("td")[index_coverage]?.innerText.includes("Individual"));
        let message_maximum = index_message_max != -1 ? row_max.querySelectorAll("td")[ index_message_max]?.innerText.trim() : undefined
        if(message_maximum.includes("Unlimited")){
          if (patient_info_extract.includes("AnnualMaximum") && max != undefined)
            rv["bk"]["AnnualMaximum"] = "Unlimited";
        }
        }
        
        
        if(index_coverage != -1 && index_type != -1){
        let row_max = rows.find(row => row.querySelectorAll("td")[index_coverage]?.innerText.includes("Individual") && 
                                            (row.querySelectorAll("td")[index_type]?.innerText.includes("Annual Maximum") ||
                                             row.querySelectorAll("td")[index_type]?.innerText.includes("DENTAL") || row.querySelectorAll("td")[index_type]?.innerText.includes("Basic Services")|| row.querySelectorAll("td")[index_type]?.innerText.includes("Dental Basic Service")));
        //console.log(row_max)
        if(row_max === undefined){
          table_maximums = Array.from(document.querySelectorAll(".well")).find(panel => panel.querySelector("legend")?.innerText.includes("Maximums - In and Out of Network"))
         //console.log(table_maximums,"orsh")
          rows = table_maximums != undefined ? Array.from(table_maximums.querySelectorAll("tr:not(.headers)")).filter(item => item?.innerText.trim() != "") : [];
         
          row_max = rows.find(row => row.querySelectorAll("td")[index_coverage]?.innerText.includes("Individual") && row.querySelectorAll("td")[index_type]?.innerText.includes("DENTAL"));
          //console.warn(row_max)
          if(row_max === undefined){
            let table_network = mode === "IN" ? "Maximums - In Network": "Maximums - Out of Network"
            table_maximums = Array.from(document.querySelectorAll(".well")).find(panel => panel.querySelector("legend")?.innerText.includes(table_network))
            //console.log(table_maximums,"orsh")
            rows = table_maximums != undefined ? Array.from(table_maximums.querySelectorAll("tr:not(.headers)")).filter(item => item?.innerText.trim() != "") : []; 
            row_max = rows.find(row => row.querySelectorAll("td")[index_coverage]?.innerText.includes("Individual") && row.querySelectorAll("td")[index_type]?.innerText.includes("DENTAL"));
            //console.warn(row_max)
        
          }
        }
        console.log(row_max,"antes")
        
        
        if(index_amount != -1 && row_max != undefined){
          max = row_max != undefined ? row_max.querySelectorAll("td")[index_amount]?.innerText.trim() : undefined;
          console.log(max)
          if (patient_info_extract.includes("AnnualMaximum") && max != undefined)
            rv["bk"]["AnnualMaximum"] = max;
        
          if (patient_info_extract.includes("DUP_AnnualMaximum") && max != undefined)
            rv["bk"]["DUP_AnnualMaximum"] =  max;
        
          if (patient_info_extract.includes("DUP_AnnualMaximum") && max != undefined)
            rv["bk"][((mode == "IN") ? "IN_AnnualMaximum" : "OON_AnnualMaximum")] =  max;
        }
        
        if(index_remaining != -1 && row_max != undefined) {
          rem = row_max != undefined ? row_max.querySelectorAll("td")[index_remaining]?.innerText.trim() : undefined;
          /*if(rem == ""){
            row_max = rows.find(row => row.querySelectorAll("td")[index_coverage]?.innerText.includes("Individual") && 
                                      row.querySelectorAll("td")[index_type]?.innerText.includes("PLEASE CALL FOR BNFT LIMITS"));
            rem = row_max != undefined ? row_max.querySelectorAll("td")[index_remaining]?.innerText.trim() : undefined;
            
          }*/
          if(rem === "") rem = "$0.00"
          if (patient_info_extract.includes("AnnualMaxRemaining") && rem != undefined && rem != "")
            rv["bk"]["AnnualMaxRemaining"] = rem;
        
          if (patient_info_extract.includes("RemainingMaximum") && rem != undefined && rem != "")
            rv["bk"]["RemainingMaximum"] = rem;
        }
        
        if(rem != undefined  && rem != "" && max != undefined && max != "" && row_max != undefined){
          if(rem === "") rem = "$0.00"
          used = formatter.format(parseFloat(max.replace(/(\$|,)/g, "")) - parseFloat(rem.replace(/(\$|,)/g, ""))); 
          
          if (patient_info_extract.includes("AmountUsedToDate")) {
            rv["bk"]["AmountUsedToDate"] = used;
          }
        
          if (patient_info_extract.includes("AnnualMaximumused")) {
            let annual_rem_value = parseFloat(rem.replace(/(\$|,)/gi, "").trim());
            let bk_rem = annual_rem_value > 0? "AnnualMaximumusedNO" :"AnnualMaximumusedYES";
            rv["bk"][bk_rem] = check;
          }
        
          if (patient_info_extract.includes("AnnMaxMet")) {
            let rem_deduc = parseFloat(rem.replace(/(\$|,)/g, ""));
            let max_met = rem_deduc <= 0 ? "AnnMaxMetYES" :"AnnMaxMetNO"
            rv["bk"][max_met] = check;
          }
        }
        
        row_max = rows.find(row => row.querySelectorAll("td")[index_coverage]?.innerText.includes("Family") && 
                                       (row.querySelectorAll("td")[index_type]?.innerText.includes("Annual Maximum") ||
                                        row.querySelectorAll("td")[index_type]?.innerText.includes("DENTAL")));
        
        if(index_amount != -1 && row_max != undefined) {
          fam_max = row_max != undefined ? row_max.querySelectorAll("td")[index_amount]?.innerText.trim() : undefined;
        
          if (patient_info_extract.includes("Annual_FamilyMaximum") && fam_max != undefined)
            rv["bk"]["Annual_FamilyMaximum"] = fam_max ;
        }
        
        }
        let index_message = headers.findIndex(item => item?.innerText.toUpperCase().includes("MESSAGE"));
        //console.log(index_message)
        let is_service = rows.some(item => item.querySelectorAll("td")[index_message]?.innerText.toUpperCase().includes("CALENDAR")  ||item.querySelectorAll("td")[index_message]?.innerText.toUpperCase() == "YEAR");
        
        if (patient_info_extract.includes("Year")) {
        if((index_message != -1 )){
            if(is_service)
              rv["bk"]["YearCalendar"] = check;
            else
              rv["bk"]["YearFiscal"] = check;
        }else if(effectivedate != ""){		  
          let start_date = effectivedate.trim();
          let regexcalendar = /^(01|1)\/\d2\/\d2,4$/;
        
          if (regexcalendar.test(start_date.trim()))
            rv["bk"]["YearCalendar"] = check;
          else if (bookmarks.includes("YearFiscal"))
            rv["bk"]["YearFiscal"] = check;
          else if (bookmarks.includes("YearPlan")) 
            rv["bk"]["YearPlan"] = check;
        }
        }
        
        if (patient_info_extract.includes("BenefitPeriod") && effectivedate != "") {
          let start_date = effectivedate.match(/\d1,\/\d1,\/\d4/gi);
          start_date = start_date != null ? start_date[0] : "";
          //console.error({start_date,is_service})
          if(is_service && !start_date.startsWith("01/01"))
            start_date = "01/01/" + new Date().getFullYear();
          
          if((/01\/01/gi).test(start_date))
            start_date = "01/01/" + new Date().getFullYear();
          
          let end_date = extractEndDate(start_date).split("/").map(item => parseInt(item) > 9 ? parseInt(item) : "0" + parseInt(item)).join("/");
          end_date= isEndDateBeforeToday(end_date) ? end_date : "";
          
          rv["bk"]["BenefitPeriod"] = start_date + " - " + end_date;
          }
        
        let index_type_ortho = headers_ortho.findIndex(item => item?.innerText.toUpperCase().includes("TYPE"));
        let index_coverage_ortho = headers_ortho.findIndex(item => item?.innerText.toUpperCase().includes("COVERAGE"));
        let index_amount_ortho = headers_ortho.findIndex(item => item?.innerText.toUpperCase().includes("AMOUNT"));
        let index_remaining_ortho = headers_ortho.findIndex(item => item?.innerText.toUpperCase().includes("REMAINING"));
        let index_message_ortho = headers_ortho.findIndex(item => item?.innerText.toUpperCase().includes("MESSAGE"))
        
        console.log(index_type_ortho)
        if(index_type_ortho == -1){
        
          table_maximums_lifetime = Array.from(document.querySelectorAll(".well")).find(panel => panel.querySelector("legend")?.innerText.includes("Maximums - In and Out of Network"))
          console.log(table_maximums_lifetime,"orsh")
          headers_ortho = table_maximums_lifetime != undefined ? Array.from(table_maximums_lifetime.querySelectorAll("th")).filter(item => item?.innerText.trim() != "") : [];
        
          rows_ortho = table_maximums_lifetime != undefined ? Array.from(table_maximums_lifetime.querySelectorAll("tr:not(.headers)")).filter(item => item?.innerText.trim() != "") : [];
          console.warn(rows_ortho)
          
          index_type_ortho = headers_ortho.findIndex(item => item?.innerText.toUpperCase().includes("TYPE"));
          index_coverage_ortho = headers_ortho.findIndex(item => item?.innerText.toUpperCase().includes("COVERAGE"));
          index_amount_ortho = headers_ortho.findIndex(item => item?.innerText.toUpperCase().includes("AMOUNT"));
          index_remaining_ortho = headers_ortho.findIndex(item => item?.innerText.toUpperCase().includes("REMAINING"));
          index_message_ortho = headers_ortho.findIndex(item => item?.innerText.toUpperCase().includes("MESSAGE"))
        
          row_max = rows_ortho.find(row => row.querySelectorAll("td")[index_coverage_ortho]?.innerText.includes("Individual") && row.querySelectorAll("td")[index_type_ortho]?.innerText.includes("Orthodontics"));
          //console.warn(row_max)
        }
        if(index_type_ortho != -1){
         
        
          row_max = rows_ortho.find(row => row.querySelectorAll("td")[index_coverage_ortho]?.innerText.includes("Individual") && 
                                        row.querySelectorAll("td")[index_type]?.innerText.includes("Orthodontics"));
          console.log(row_max)
        
          if(row_max === undefined){
            table_maximums_lifetime = Array.from(document.querySelectorAll(".well")).find(panel => panel.querySelector("legend")?.innerText.includes("Maximums - In and Out of Network"))
            console.log(table_maximums_lifetime,"orsh")
            rows_ortho = table_maximums_lifetime != undefined ? Array.from(table_maximums_lifetime.querySelectorAll("tr:not(.headers)")).filter(item => item?.innerText.trim() != "") : [];
            console.warn(rows_ortho)
            row_max = rows_ortho.find(row => row.querySelectorAll("td")[index_coverage_ortho]?.innerText.includes("Individual") && row.querySelectorAll("td")[index_type_ortho]?.innerText.includes("Orthodontics"));
            console.warn(row_max)
          }
        
          if(index_amount_ortho != -1 && row_max != undefined){
        
              ortho_max = row_max != undefined ? row_max.querySelectorAll("td")[index_amount_ortho]?.innerText.trim() : undefined;
          if(ortho_max.includes("$") && ortho_max)
              if (patient_info_extract.includes("LifetimeMax") && ortho_max != undefined)
                  rv["bk"]["LifetimeMax"] = ortho_max;
        
              if (patient_info_extract.includes("DUP_LifetimeMax") && ortho_max != undefined)
                  rv["bk"]["DUP_LifetimeMax"] =  ortho_max;
          }
        
          if(index_remaining_ortho != -1 && row_max != undefined) {
            ortho_rem = row_max != undefined ? row_max.querySelectorAll("td")[index_remaining_ortho]?.innerText.trim() : undefined;
            if(ortho_rem === "") ortho_rem = "$0.00"
            if(ortho_rem.includes("$") && ortho_rem){
              if (patient_info_extract.includes("Orthodontics_Remaining") && ortho_rem != undefined)
                rv["bk"]["Orthodontics_Remaining"] = ortho_rem;
        
              if (patient_info_extract.includes("Remaining") && ortho_rem != undefined)
                rv["bk"]["Remaining"] = ortho_rem;
            }
            
          }
        
          if(ortho_rem != undefined && ortho_max != undefined && row_max != undefined){
          if(ortho_max.includes("$") && ortho_rem.includes("$")){
            ortho_used = formatter.format(parseFloat(ortho_max.replace(/(\$|,)/g, "")) - parseFloat(ortho_rem.replace(/(\$|,)/g, ""))); 
            if(patient_info_extract.includes("IsLifetimeMaxUsed")){
              if(ortho_used.includes("$0.00")){
                rv["bk"]["IsLifetimeMaxUsedNO"] = check
              }else{
                rv["bk"]["IsLifetimeMaxUsedYES"] = check
              }
            }
            if (patient_info_extract.includes("Orthodontics_AmountUsedToDate"))
              rv["bk"]["Orthodontics_AmountUsedToDate"] = ortho_used;
        
          }
        
        
        }
         if(row_max  && index_message != -1){
          let benefit_ortho = row_max != undefined ? row_max.querySelectorAll("td")[index_message]?.innerText.trim() : undefined;
          //console.log(benefit_ortho)
            if(benefit_ortho && benefit_ortho.includes("Lifetime") && bookmarks.includes("Orthodontics_BenefitperiodLifetime")){
              rv["bk"]["Orthodontics_BenefitperiodLifetime"]= check;
            }
            if(benefit_ortho && benefit_ortho.includes("Calendar") && bookmarks.includes("Orthodontics_BenefitperiodCalendar")){
              rv["bk"]["Orthodontics_BenefitperiodCalendar"]= check;
            }
            if(benefit_ortho && patient_info_extract.includes("IsLifetimeMax")){
              if(benefit_ortho.includes("Lifetime")){
                rv["bk"]["IsLifetimeMaxYES"] = check
              }else{
                rv["bk"]["IsLifetimeMaxNO"] = check
        
              }
        
            }
          }
        }
        //Get Deductibles Information OON ----------------------------------------------------------------------------------------------
        let table_deductible_OON = Array.from(document.querySelectorAll(".well")).find(panel => panel.querySelector("legend")?.innerText.toUpperCase().includes("OUT ") && panel.querySelector("legend")?.innerText.toUpperCase().includes("DEDUCTIBLES"));
        headers_ded = table_deductible_OON != undefined ? Array.from(table_deductible_OON.querySelectorAll("th")).filter(item => item?.innerText.trim() != "") : [];
        rows_ded = table_deductible_OON != undefined ? Array.from(table_deductible_OON.querySelectorAll("tr:not(.headers)")).filter(item => item?.innerText.trim() != "") : [];
        
        index_type = headers_ded.findIndex(item => item?.innerText.toUpperCase().includes("TYPE"));
        index_coverage = headers_ded.findIndex(item => item?.innerText.toUpperCase().includes("COVERAGE"));
        index_amount = headers_ded.findIndex(item => item?.innerText.toUpperCase().includes("AMOUNT"));
        index_remaining = headers_ded.findIndex(item => item?.innerText.toUpperCase().includes("REMAINING"));
        
        let deduc_OON = "";
        let rem_deduc_OON = "";
        
        let fam_deduc_OON = "";
        let fam_rem_deduc_OON = "";
        
        if(index_coverage != -1){
        let row_ded = rows_ded.find(row => row.querySelectorAll("td")[index_coverage]?.innerText.includes("Individual") && 
                                            !row.querySelectorAll("td")[index_type]?.innerText.includes("Ortho"));
        
        if(index_amount != -1 && rows_ded != undefined) {
          deduc_OON = row_ded != undefined ? row_ded.querySelectorAll("td")[index_amount]?.innerText.trim() : undefined;
        
          if (patient_info_extract.includes("Deductible_OON") && deduc != undefined)
            rv["bk"]["Deductible_OON"] = deduc_OON;
        }
        
        if(index_remaining != -1 && rows_ded != undefined) {
          rem_deduc = row_ded != undefined ? row_ded.querySelectorAll("td")[index_remaining]?.innerText.trim() : undefined;
        
          if (patient_info_extract.includes("RemainingDeductible_OON") && rem_deduc_OON != undefined)
            rv["bk"]["RemainingDeductible_OON"] = rem_deduc_OON;
        }
        
        row_ded = rows_ded.find(row => row.querySelectorAll("td")[index_coverage]?.innerText.includes("Family") && 
                                        !row.querySelectorAll("td")[index_type]?.innerText.includes("Ortho"));
        
        if(index_amount != -1 && rows_ded != undefined) {
          fam_deduc_OON = row_ded != undefined ? row_ded.querySelectorAll("td")[index_amount]?.innerText.trim() : undefined;
        
          if (patient_info_extract.includes("Family_OON") && fam_deduc_OON != undefined)
            rv["bk"]["Family_OON"] = fam_deduc_OON ;
        }
        
        if(index_remaining != -1 && rows_ded != undefined) {
          fam_rem_deduc_OON = row_ded != undefined ? row_ded.querySelectorAll("td")[index_remaining]?.innerText.trim() : undefined;
        
          if (patient_info_extract.includes("Remaining_FamilyDeductible_OON") && fam_rem_deduc_OON != undefined)
            rv["bk"]["Remaining_FamilyDeductible_OON"] = fam_rem_deduc_OON;
        }
        }
        
        let table_maximums_OON = Array.from(document.querySelectorAll(".well")).find(panel => panel.querySelector("legend")?.innerText.toUpperCase().includes(mode) && panel.querySelector("legend")?.innerText.toUpperCase().includes("MAXIMUMS"));
        headers = table_maximums_OON != undefined ? Array.from(table_maximums_OON.querySelectorAll("th")).filter(item => item?.innerText.trim() != "") : [];
        rows = table_maximums_OON != undefined ? Array.from(table_maximums_OON.querySelectorAll("tr:not(.headers)")).filter(item => item?.innerText.trim() != "") : [];
        
        index_type = headers.findIndex(item => item?.innerText.toUpperCase().includes("TYPE"));
        index_coverage = headers.findIndex(item => item?.innerText.toUpperCase().includes("COVERAGE"));
        index_amount = headers.findIndex(item => item?.innerText.toUpperCase().includes("AMOUNT"));
        index_remaining = headers.findIndex(item => item?.innerText.toUpperCase().includes("REMAINING"));
        
        let max_OON = "";
        let rem_OON = "";
        
        if(index_coverage != -1 && index_type != -1){
          let row_max = rows.find(row => row.querySelectorAll("td")[index_coverage]?.innerText.includes("Individual") && 
                                              (row.querySelectorAll("td")[index_type]?.innerText.includes("Annual Maximum") ||
                                              row.querySelectorAll("td")[index_type]?.innerText.includes("DENTAL") || row.querySelectorAll("td")[index_type]?.innerText.includes("Basic Services")));
        
          if(index_amount != -1 && row_max != undefined){
            max_OON = row_max != undefined ? row_max.querySelectorAll("td")[index_amount]?.innerText.trim() : undefined;
        
            if (patient_info_extract.includes("AnnualMaximum_OON") && max_OON != undefined)
              rv["bk"]["AnnualMaximum_OON"] = max_OON;
          }
        
          if(index_remaining != -1 && row_max != undefined) {
            rem_OON = row_max != undefined ? row_max.querySelectorAll("td")[index_remaining]?.innerText.trim() : undefined;
        
            if (patient_info_extract.includes("RemainingMaximum_OON") && rem_OON != undefined)
              rv["bk"]["RemainingMaximum_OON"] = rem_OON;
        
          }
        }
        console.log(rv)
        return rv;""",current_row, is_plan_hmo, patient_name, configP, patient_last_name, returned_values, bot_name, plan_medicare)
        returned_values = returned_values.decode()
        returned_values = bot.driver.execute_script(r"""        const current_row = arguments[1];
        const is_plan_hmo = arguments[2];
        const configP = arguments[3];
        const returned_values = arguments[4];
        const bot_name = arguments[5];
        const plan_medicare = arguments[6];
        let rv = returned_values;
        let clinic_onn=["clinic#vigp","Southern Pines Smiles"]
        let patient_info_extract = configP["data"]["patient_info_extract"];
        let mode = "IN";
        
        if (configP["network_mode"] == "OON") 
            mode = "OUT";
          
          
        if ((configP["client_name"] == "Ruby Canyon Dental" || clinic_onn.includes(configP["clinic_name"]))&& configP["bot_name"]["specific_plan_type"] != '')
            mode = configP["bot_name"]["specific_plan_type"] == "OON" ? "OUT" : "INN";
        if(configP["bot_name"]["specific_plan_type"] != "")configP["bot_name"]["specific_plan_type"] === "INN" ? "IN":"OUT OF"
        }
        if(configP["client_name"]== "RevenueWell"){
            let net_mode = current_row[1];
            if (net_mode.includes("OON")) mode ="OUT" 
        }
        if(configP['clinic_name']== "Johnston Smiles"){
            let net_mode = current_row[29];
            if (net_mode.includes("OON")) mode ="OUT" 
        }
          
        if(configP["client_name"]== "DentalDepot"){
            let is_plan_hmo = "is_plan_hmo";
            if (is_plan_hmo.includes("OON") && "plan_medicare" === "False") mode ="OUT"
        }
        
        let table_coinsurance = Array.from(document.querySelectorAll(".well")).find(panel => panel.querySelector("legend")?.innerText.toUpperCase().includes(mode) && panel.querySelector("legend")?.innerText.toUpperCase().includes("CO-INSURANCE"));
        headers = table_coinsurance != undefined ? Array.from(table_coinsurance.querySelectorAll("th")).filter(item => item?.innerText.trim() != "") : [];
        rows = table_coinsurance != undefined ? Array.from(table_coinsurance.querySelectorAll("tr:not(.headers)")).filter(item => item?.innerText.trim() != "") : [];
        let index_type= headers.findIndex(item => item?.innerText.toUpperCase().includes("TYPE"));
        let index_coverage_percentage = headers.findIndex(item => item?.innerText.toUpperCase().includes("PERCENTAGE"));
        console.log(table_coinsurance)
        
        for (const row of rows) {
            const typeCell = row.querySelectorAll("td")[index_type];
            const coverageCell = row.querySelectorAll("td")[index_coverage_percentage];
            if (typeCell?.innerText.includes("Ortho")) {
                if (patient_info_extract.includes("DUP_Orthodontic") && rv["bk"]["DUP_Orthodontic"] == undefined ) {
                    rv["bk"]["DUP_Orthodontic"] = coverageCell?.innerText.split("/")[1]
                }
                if (patient_info_extract.includes("Orthodontic") && rv["bk"]["Orthodontic"] == undefined ) {
                    rv["bk"]["Orthodontic"] = coverageCell?.innerText.split("/")[1]
                }
            }
        
            if (typeCell?.innerText.includes("Major")) {
                if (patient_info_extract.includes("Major") && rv["bk"]["Major"] == undefined ) {
                    rv["bk"]["Major"] = coverageCell?.innerText.split("/")[1]
                }
                if (patient_info_extract.includes("DUP_Major") && rv["bk"]["DUP_Major"] == undefined ) {
                    rv["bk"]["DUP_Major"] = coverageCell?.innerText.split("/")[1]
                }
            }
            if (typeCell?.innerText.includes("Basic")) {
        		console.log(coverageCell?.innerText.split("/")[1])
                if (patient_info_extract.includes("Basic") && rv["bk"]["Basic"] == undefined ) {
                    rv["bk"]["Basic"] = coverageCell?.innerText.split("/")[1]
                }
                if (patient_info_extract.includes("DUP_Basic") && rv["bk"]["DUP_Basic"] == undefined ) {
                    rv["bk"]["DUP_Basic"] = coverageCell?.innerText.split("/")[1]
                }
            }
            if (typeCell?.innerText.includes("Preventative")) {
                if (patient_info_extract.includes("Preventive") && rv["bk"]["Preventive"] == undefined ) {
                    rv["bk"]["Preventative"] = coverageCell?.innerText.split("/")[1]
                }
                if (patient_info_extract.includes("DUP_Preventive") && rv["bk"]["DUP_Preventive"] == undefined ) {
                    rv["bk"]["DUP_Preventive"] = coverageCell?.innerText.split("/")[1]
                }
            }
        }
        
        return rv""",current_row, is_plan_hmo, configP, returned_values, bot_name, plan_medicare)
        returned_values = returned_values.decode()
        returned_values = returned_values.decode()
        returned_values = bot.driver.execute_script(r"""        const returned_values = arguments[1];
        const patient_dob = arguments[2];
        const configP = arguments[3];
        function calcularEdad(fecha) {
            let hoy = new Date();
            let cumpleanos = new Date(fecha);
            let edad = hoy.getFullYear() - cumpleanos.getFullYear();
            let m = hoy.getMonth() - cumpleanos.getMonth();
        
            if (m < 0 || (m === 0 && hoy.getDate() < cumpleanos.getDate())) {
                edad--;
            }
        
            return edad;
        }
        
        let rv = returned_values;
        let patient_info_extract = configP["data"]["patient_info_extract"];
        
        if(patient_info_extract.includes("PatientAddress") && rv["bk"]["PatientAddress"] == undefined){
            let indexaddr = Array.from(document.querySelectorAll("#longProcessPage table td")).findIndex(row => row.innerText.includes('Address'));
            let address = indexaddr != -1 ? Array.from(document.querySelectorAll("#longProcessPage table td"))[indexaddr + 1].innerText.trim() : "";
        
            if(address != "")
                rv["bk"]["PatientAddress"] = address;
        }
        
        if(patient_info_extract.includes("Age") && !values[0].includes("Age")){
            let age = calcularEdad("patient_dob");
        
            if(age > 0)
                rv["bk"]["Age"] = age;
        }
        
        return rv;""",returned_values, patient_dob, configP)
        returned_values = returned_values.decode()
        time.sleep(float(2))
        bot.scrap.load_url("{urlSearch}")
        bot.scrap.wait_for_object("present","id","longProcessPage",30)
        time.sleep(5)
        if len(configP["data"]["deductible_applies"]) == 0 or configP["client_name"] in not_clients_deductible:
            bot.driver.execute_script(r"""            
            document.querySelectorAll(".fl input")[1].click();""")
            time.sleep(2)
            bot.scrap.wait_for_object("visible","id","category",5)
            time.sleep(3)
            CategoryOptions = bot.driver.execute_script(r"""            
            
            const selectedValues = Array.from(document.querySelectorAll("#category option"))
              .filter((option) => option.innerText !== "Choose One")
              .map((option) => option.value);
            
            console.log(selectedValues);
            return selectedValues""")
            CategoryOptions = CategoryOptions.decode()
            for i in range(len(CategoryOptions)):
                Options = i + 1
                bot.driver.execute_script(r"""                const Options = arguments[1];
                document.querySelector('#category option[value="Options"]').selected = true
                let button_vien_benefits = Array.from(document.querySelectorAll("a[id*='id']")).find(item => item.innerText.trim() != "" ? item.innerText.trim().includes("View Benefits") : false);
                if(button_vien_benefits)
                	button_vien_benefits.click();""",Options)
                time.sleep(2)
                bot.scrap.wait_for_object("not_visible","tag","div[id*='ajax-indicator-veil']",30)
                time.sleep(3)
                time.sleep(2)
                error_title = bot.scrap.wait_for_object("visible","tag","li[class='alert-error']",10)
                if error_title:
                    attemps = 1
                    while attemps > 0:
                        bot.driver.execute_script(r"""                        
                        
                        let button_vien_benefits = Array.from(document.querySelectorAll("a[id*='id']")).find(item => item.innerText.trim() != "" ? item.innerText.trim().includes("View Benefits") : false);
                        
                        if(button_vien_benefits != undefined)
                        	button_vien_benefits.click();""")
                        time.sleep(2)
                        bot.scrap.wait_for_object("not_visible","tag","div[id*='ajax-indicator-veil']",30)
                        time.sleep(3)
                        time.sleep(2)
                        error_title = bot.scrap.wait_for_object("visible","tag","li[class='alert-error']",10)
                        attemps = 1 if error_title else 0
                returned_values = bot.driver.execute_script(r"""                const gsheet_columns = arguments[1];
                const Options = arguments[2];
                const found_codes = arguments[3];
                const current_row = arguments[4];
                const is_plan_hmo = arguments[5];
                const configP = arguments[6];
                const returned_values = arguments[7];
                const bot_name = arguments[8];
                const plan_medicare = arguments[9];
                function extraerTablas(tbody) {
                    var tabla_extraida = []
                    Array.from(tbody).forEach(function (row) {
                        if (row.cells.length > 0) {
                            tabla_extraida.push([]);
                            Array.from(row.cells).forEach(function (cell) {
                                tabla_extraida[tabla_extraida.length - 1].push(cell.innerText);
                            })
                        }
                    })
                    return tabla_extraida
                  }
                    let rv = returned_values;
                    //let rv = }
                    let not_covered_codes = {procedures_not_covered};
                    //let found_codes =found_codes;
                    let check = "n";
                    let columns = gsheet_columns
                    let row = current_row
                    const   patient_info_extract = configP["data"]["patient_info_extract"],
                            no_covered_cases = configP["data"]["no_covered_cases"],
                            busqueda = configP["data"]["busqueda"],
                            percentage_case = configP["data"]["percentage_case"],
                            frequency_written_case = configP["data"]["frequency_written_case"],
                            dup_frequency_written_case =configP["data"]["dup_frequency_written_case"],
                            age_limit_cases = configP ["data"]["age_limit_case"],
                            bookmarks = configP["data"]["bookmarks"],
                            deductible_applies =configP["data"]["deductible_applies"],
                            eligible_cases = configP["data"]["eligible_cases"],
                            specific_teeth_case = configP["data"]["specific_teeth_case"],
                            unrestored_case = configP["data"]["unrestored_case"],
                            share_cases = configP["data"]["share_cases"],
                            specific_share_case = configP["data"]["specific_share_case"],
                            last_perform_cases = configP ["data"]["last_perform_case"],
                            oon_percentage_case = configP ["data"]["oon_percentage_case"],
                            preventive_basic_case = configP ["data"]["preventive_basic_case"],
                            downgrade_case_select = configP["data"]["downgrade_case_select"];
                    let     table = null,
                            mode = "IN",
                            is_deductible = false,
                            is_applies_to_max = false,
                            percentage_D7210 = "",
                            percentage_D7140 = "",
                            table_coverage = [],
                            table_coverage_oon =[],
                            table_coverage_both = [],
                            is_covered = true
                            headers =[],
                            headers_in_out =[],
                            matched_age = null,
                            matched_tooth = null,
                            matched_freq = null;
                    const frequency_regex = /Frequency:\s*(.*?(?:allowed|period|placement|per tooth|per arch|lifetime|years|Months|Year|MOUTH))/;
                    const age_regex = /Age Limitation:\s*Maximum Age:\s*(\d+)/;
                    const tooth_regex = /TOOTH NUMBER\s+([\d\sTO]+)(?=\s|\.|$)/;
                
                
                
                
                  if(configP["bot_name"]["specific_plan_type"] != "")configP["bot_name"]["specific_plan_type"] === "INN" ? "IN":"OUT OF"
                  }
                  if(configP["client_name"]== "RevenueWell"){
                    let net_mode = current_row[1];
                    if (net_mode.includes("OON")) mode ="OUT OF" 
                  }
                  if(configP["clinic_name"]== "Johnston Smiles"){
                    let net_mode = current_row[29];
                    if (net_mode.includes("OON")) mode ="OUT OF" 
                  }
                  if(configP["client_name"]== "DentalDepot"){
                    let is_plan_hmo = "is_plan_hmo";
                    if (is_plan_hmo.includes("OON") && "plan_medicare" === "False") mode ="OUT OF" 
                  
                  }
                  Array.from(document.querySelectorAll("legend")).forEach(head => {
                    console.log(mode)
                    if(head.innerText.toUpperCase().includes(`SERVICE LEVEL BENEFITS - ${mode} NETWORK`)){
                        headers = Array.from(head.nextElementSibling.querySelector("table tbody").querySelectorAll("th")).filter(item => item?.innerText.trim() != "");
                        table = head.nextElementSibling.querySelector("table tbody");
                        table_coverage = extraerTablas(table.children);
                        console.warn(table_coverage)
                    }
                    if(head.innerText === "Service Level Benefits - In and Out of Network"){
                        headers_in_out = Array.from(head.nextElementSibling.querySelector("table tbody").querySelectorAll("th")).filter(item => item?.innerText.trim() != "");
                        table = head.nextElementSibling.querySelector("table tbody");
                        table_coverage_both = extraerTablas(table.children);
                        console.error(table_coverage_both)
                    }
                    if(head.innerText === "Service Level Benefits - Out of Network"){
                       
                        table = head.nextElementSibling.querySelector("table tbody");
                        table_coverage_oon = extraerTablas(table.children);
                        
                    }
                    if(head.innerText.toUpperCase().includes(`DEDUCTIBLES - ${mode}`)){
                        is_deductible = true
                    }
                    if(head.innerText.toUpperCase().includes(`MAXIMUMS - ${mode}`)){
                        is_applies_to_max = true
                    }
                  
                  });
                  
                  let index_message = headers.findIndex(item => item?.innerText.toUpperCase().includes("MESSAGE"));
                  let index_code = headers.findIndex(item => item?.innerText.toUpperCase().includes("CODE"));
                  let index_frequency = headers.findIndex(item => item?.innerText.toUpperCase().includes("FREQUENCY"));
                  let index_percentage = headers.findIndex(item => item?.innerText.toUpperCase().includes("PERCENTAGE"));
                
                  if (table_coverage.length > 0) {
                    for(row of table_coverage){
                        
                        if(index_frequency != -1 && row[index_frequency]?.trim()){
                            
                            matched_freq = frequency_regex.exec(row[index_frequency]?.trim());
                            matched_tooth = tooth_regex.exec(row[index_frequency]?.trim());
                            matched_age = age_regex.exec(row[index_frequency]?.trim())
                            console.warn({matched_freq,matched_age,matched_tooth})
                        }
                     
                        if (index_message !== -1 && row[index_message]?.trim() && row[index_message].includes("Not Covered")) {
                            not_covered_codes.push(row[index_code]);
                        }
                        const percentageValue = row[index_percentage]?.trim();
                        if (/(\d+)%\s*\/\s*(\d+)%/.test(percentageValue) || percentageValue?.includes("Not Covered")) {
                            SetCoverageandPercentage(row[index_code], percentageValue);
                            SetDeductible(row[index_code], is_deductible);
                            SetAppliestoMax(row[index_code], is_applies_to_max);
                        }
                        if (matched_tooth) {
                            if (specific_teeth_case.includes(row[index_code]) && matched_tooth[1]) {
                                rv['bk'][`${row[index_code]}_Specificteethcov`] = matched_tooth[1].trim();
                            }
                            if (downgrade_case_select.includes(row[index_code]) && row[index_message]?.toLowerCase().includes("alternate benefits may apply")) {
                                rv['bk'][`${row[index_code]}_DowngradeYES`] = check;
                            }
                            if (bookmarks.includes(row[index_code]+"_downgradedto") && row[index_message]?.toLowerCase().includes("alternate benefits may apply")) {
                                rv['bk'][`${row[index_code]}_downgradedto`] = "YES";
                            }
                        }
                        if (matched_freq) {
                            SetFrequency(row[index_code], matched_freq[1]);
                        }
                        if (matched_age) {
                            SetAge(row[index_code], matched_age[1]);
                        }
                        if (index_message !== -1 && row[index_message]?.includes("Shares frequency with") && specific_share_case.includes(row[index_code])) {
                            SetSharedCase(row[index_code], row[index_message]);
                        }
                    
                        if (index_frequency !== -1 && row[index_frequency]?.includes("History")) {
                            SetLastPerformed(row[index_code], row[index_frequency]);
                        }
                
                    }
                  }
                  if(table_coverage_oon.length > 0){
                    let index_code = table_coverage_oon[1].findIndex((i) => i.includes("Procedure Code"));
                    for(row of table_coverage_oon){
                        if(/(\d+)%\s*\/\s*(\d+)%/.test(row[index_code+1])){
                          //console.log(row[0], row[1])
                            SetPercentageOON(row[index_code],row[index_code+1])
                        }
                    }
                  }
                  if (table_coverage_both.length > 0) {
                    
                    index_message = headers_in_out.findIndex(item => item?.innerText.toUpperCase().includes("MESSAGE"));
                    index_code = headers_in_out.findIndex(item => item?.innerText.toUpperCase().includes("CODE"));
                    index_frequency = headers_in_out.findIndex(item => item?.innerText.toUpperCase().includes("FREQUENCY"));
                    index_percentage = headers_in_out.findIndex(item => item?.innerText.toUpperCase().includes("PERCENTAGE"));
                    
                
                  
                  
                    for(row of table_coverage_both){
                        matched_freq = frequency_regex.exec(row[index_frequency]?.trim());
                        matched_tooth = tooth_regex.exec(row[index_frequency]?.trim());
                        matched_age = age_regex.exec(row[index_frequency]?.trim());
                        if (index_message !== -1 && row[index_message]?.trim() && row[index_message].includes("Not Covered")) {
                            not_covered_codes.push(row[index_code]);
                            is_covered = false;
                            if (no_covered_cases.includes(row[index_code])) {
                                rv["bk"][`${row[index_code]}_NoCovered`] = check;
                            }
                        } else {
                            is_covered = true;
                        }
                    
                        if (is_covered && row[index_code]) {
                            if ((table_coverage_oon.length === 0 || oon_percentage_case.includes(row[index_code])) && !rv["bk"][`${row[index_code]}_Percentage_OON`]) {
                                if (/(\d+)%\s*\/\s*(\d+)%/.test(row[index_percentage])) {
                                    SetPercentageOON(row[index_code], row[index_percentage]);
                                }
                            }
                    
                            if ((table_coverage.length === 0 || row[index_percentage]?.trim() && percentage_case.includes(row[index_code])) && !rv["bk"][`${row[index_code]}_Percentage`]) {
                                if (/(\d+)%\s*\/\s*(\d+)%/.test(row[index_percentage]) ||  row[index_percentage]?.includes("Not Covered")) {
                                    SetCoverageandPercentage(row[index_code], row[index_percentage]);
                                    SetDeductible(row[index_code], is_deductible);
                                    SetAppliestoMax(row[index_code], is_applies_to_max);
                                    //found_codes.push(row[index_code]);
                                }
                            }
                            if (matched_tooth) {
                                if (specific_teeth_case.includes(row[index_code]) && matched_tooth[1]) {
                                    rv['bk'][`${row[index_code]}_Specificteethcov`] = matched_tooth[1].trim();
                                }
                                if (downgrade_case_select.includes(row[index_code]) && row[index_message]?.toLowerCase().includes("alternate benefits may apply")) {
                                    rv['bk'][`${row[index_code]}_DowngradeYES`] = check;
                                }
                                if (downgrade_case_select.includes(row[index_code]) && row[index_message]?.toLowerCase().includes("alternate benefits may apply")) {
                                    rv['bk'][`${row[index_code]}_DowngradeYES`] = check;
                                }
                            }
                            if (matched_freq) {
                                SetFrequency(row[index_code], matched_freq[1]);
                            }
                            if (matched_age) {
                                SetAge(row[index_code], matched_age[1]);
                            }
                            if (index_message !== -1 && row[index_message]?.includes("Shares frequency with") && specific_share_case.includes(row[index_code])) {
                                SetSharedCase(row[index_code], row[index_message]);
                            }
                            if (index_frequency !== -1 && row[index_frequency]?.includes("History")) {
                                SetLastPerformed(row[index_code], row[index_frequency]);
                            }
                        }
                           
                    }
                  }
                  function SetPercentageOON(code, percentage){
                    if (percentage ){
                        percentage = percentage.split("/")[1].trim()
                        
                        if (oon_percentage_case.includes(code)){
                            rv['bk'][code + "_Percentage_OON"] = percentage
                        }
                        if (patient_info_extract.includes("OON_Basic") && code == "D2140") {
                            rv["bk"]["OON_Basic"] = percentage
                        }
                        if (patient_info_extract.includes("OON_Preventive") && code == "D1110") {
                            rv["bk"]["OON_Preventive"] = percentage
                        }
                        if (patient_info_extract.includes("OON_Diagnostic") && code == "D0120") {
                            rv["bk"]["OON_Diagnostic"] = percentage
                        }
                        if (patient_info_extract.includes("OON_Major") && code == "D2740") {
                            rv["bk"]["OON_Major"] = percentage
                        }
                        if (patient_info_extract.includes("OON_Orthodontic") && code == "D8080") {
                            rv["bk"]["OON_Orthodontic"] = percentage
                        }
                        if (patient_info_extract.includes("OON_Periodontal") && code == "D4341") {
                            rv["bk"]["OON_Periodontal"] = percentage
                        }
                        if (patient_info_extract.includes("OON_Endodontic") && code == "D3310") {
                            rv["bk"]["OON_Endodontic"] = percentage
                        }
                        if (patient_info_extract.includes("OON_OralSX") && code == "D4341") {
                            rv["bk"]["OON_OralSX"] = percentage
                        }
                        if (patient_info_extract.includes("OON_Implants") && code == "D6010") {
                            rv["bk"]["OON_Implants"] = percentage
                        }
                        if (patient_info_extract.includes("OON_Prosthodontics") && code == "D5110") {
                            rv["bk"]["OON_Prosthodontics"] = percentage
                        }
                        if (patient_info_extract.includes("OON_AdjunctiveGeneral") && code == "D4D9110341") {
                            rv["bk"]["OON_AdjunctiveGeneral"] = percentage
                        }
                    
                    }
                  }
                  function SetCoverageandPercentage(code,percentage){
                    if (percentage ){
                        console.log(percentage)
                        if(percentage.includes("$") || percentage.includes("%")) {
                            percentage =percentage.replace(/
                ?\$\d+(\.\d2)?/, '')
                            percentage = percentage.split("/")[1].trim()
                        }
                        
                        if (percentage_case.includes(code)){
                            rv['bk'][code + "_Percentage"] = percentage
                           // found_codes.push(code)
                        }
                        if (percentage_case.includes("DUP_" + code)){
                            rv['bk']["DUP_" + code + "_Percentage"] = percentage
                        }
                        if(bookmarks.includes(code + "_FallsunderDental") && mode.includes("IN")){
                            rv["bk"][code  + "_FallsunderDental"] = check;
                        }
                        if(code == "D7140")
                            percentage_D7140 = percentage;
                  
                        if(code == "D7210")
                            percentage_D7210 = percentage;
                        //console.log(patient_info_extract.includes("SimpleOralSX"))
                        if (patient_info_extract.includes("SimpleOralSX") && rv["bk"]["SimpleOralSX"] == undefined  && code == "D7140"){
                            rv["bk"]["SimpleOralSX"] = percentage
                        }
                        if (patient_info_extract.includes("OralSX") && rv["bk"]["OralSX"] == undefined  && code == "D7210"){
                            rv["bk"]["OralSX"] = percentage
                        }
                        
                        if (patient_info_extract.includes("Preventive") && rv["bk"]["Preventive"] == undefined  && code == "D1110") {
                            rv["bk"]["Preventive"] = percentage
                            
                        }
                        if (patient_info_extract.includes("Orthodontic") && rv["bk"]["Orthodontic"] == undefined  && code == "D8080") {
                            rv["bk"]["Orthodontic"] = percentage
                        }
                        
                        if (patient_info_extract.includes("Orthodontics_Coverage")  && code == "D8080") {
                            rv["bk"]["Orthodontics_CoverageYES"] = check
                        }
                        if (patient_info_extract.includes("Diagnostic") && rv["bk"]["Diagnostic"] == undefined  && code == "D0120") {
                            rv["bk"]["Diagnostic"] = percentage
                        }
                  
                        if (patient_info_extract.includes("Periodontal") && rv["bk"]["Periodontal"] == undefined && code == "D4341") {
                            rv["bk"]["Periodontal"] = percentage
                            let percentage_found = parseInt(percentage);
                            if (percentage_found >= 61 && percentage_found < 90) {
                                if(bookmarks.includes("Periodontal_BASIC"))
                                    rv["bk"]["Periodontal_BASIC"] = check;
                                //Otherwise it's Major
                            } else {
                                if(bookmarks.includes("Periodontal_MAJOR"))
                                    rv["bk"]["Periodontal_MAJOR"] = check;
                            }
                        }
                        if ((patient_info_extract.includes("Endodontic") && rv["bk"]["Endodontic"] == undefined  && (code == "D3310" || code == "D3330"))) {
                            rv["bk"]["Endodontic"] = percentage
                            let percentage_found = parseInt(percentage);
                            if (percentage_found >= 61 && percentage_found < 90) {
                                if(bookmarks.includes("Endodontic_BASIC"))
                                    rv["bk"]["Endodontic_BASIC"] = check;
                                //Otherwise it's Major
                            } else {
                                if(bookmarks.includes("Endodontic_MAJOR"))
                                    rv["bk"]["Endodontic_MAJOR"] = check;
                            }
                        }
                        if (patient_info_extract.includes("Orthodontics_Pays") && rv["bk"]["Orthodontics_Pays"] == undefined && code == "D8090") {
                            rv["bk"]["Orthodontics_Pays"] = percentage
                        }
                        if (patient_info_extract.includes("Implants") && rv["bk"]["Implants"] == undefined  && code == "D6010") {
                            rv["bk"]["Implants"] = percentage
                        }
                        if(configP["client_name"] == "Today`s Dental PC"){
                            if(["D9110", "D9230", "D9944"].includes(code) && patient_info_extract.includes("AdjunctiveGeneral") && rv["bk"]["AdjunctiveGeneral"] == undefined ){
                                if(rv["bk"]["AdjunctiveGeneral"] != undefined){
                                    if(parseInt(percentage) < parseInt(rv["bk"]["AdjunctiveGeneral"]))
                                        rv["bk"]["AdjunctiveGeneral"] = percentage;
                                }else
                                    rv["bk"]["AdjunctiveGeneral"] = percentage;
                            }
                        }else{
                            if (patient_info_extract.includes("AdjunctiveGeneral") && rv["bk"]["AdjunctiveGeneral"] == undefined  && code == "D9110") {
                                rv["bk"]["AdjunctiveGeneral"] = percentage
                            }
                        }
                        if (patient_info_extract.includes("Major") && code == "D2740" && rv["bk"]["Major"] == undefined ) {
                            rv["bk"]["Major"] = percentage
                        }
                        if (patient_info_extract.includes("Basic") && (code == "D2140" || code == "D2391") && rv["bk"]["Basic"] == undefined ) {
                            rv["bk"]["Basic"] = percentage
                        }
                        if(code == "D2391" && patient_info_extract.includes("PostCompCovd")){
                            let bk = percentage ? "PostCompCovdYES" : "PostCompCovdNO"
                            rv['bk'][bk] = check
                        }
                        if (patient_info_extract.includes("Prosthodontics") && code == "D5110" && rv["bk"]["Prosthodontics"] == undefined ) {
                            rv["bk"]["Prosthodontics"] = percentage
                        }
                  
                        /**************** DUP CATEGORY ********************************************/
                        if (patient_info_extract.includes("DUP_Basic") && code == "D2140" && rv["bk"]["DUP_Basic"] == undefined) {
                            rv["bk"]["DUP_Basic"] = percentage
                        }
                        if (patient_info_extract.includes("DUP_Major") && code == "D2740" && rv["bk"]["DUP_Major"] == undefined ) {
                            rv["bk"]["DUP_Major"] = percentage
                        }
                        if (patient_info_extract.includes("DUP_Orthodontic") && code == "D8080" && rv["bk"]["DUP_Orthodontic"] == undefined ) {
                            rv["bk"]["DUP_Orthodontic"] = percentage
                        }
                        if (preventive_basic_case.includes(code) && parseInt(percentage) >= 0) {
                            console.log("here")
                            //console.error(rv["bk"]["Preventive"].replace("%","").trim())
                            let preventive_per = rv["bk"]["Preventive"] != undefined ?parseInt(rv["bk"]["Preventive"].replace("%","").trim()):90
                            let basic_per=rv["bk"]["Basic"] != undefined ? parseInt(rv["bk"]["Basic"].replace("%","").trim()):60
                            let major_per=rv["bk"]["Major"] != undefined ? parseInt(rv["bk"]["Major"].replace("%","").trim()):50
                            let is_equal_percentage = basic_per == major_per
                            console.log(preventive_per,basic_per,major_per)
                            if(is_equal_percentage){
                                if(parseInt(percentage)>=70 )rv["bk"][code+"_Basic"] = check
                                else if(parseInt(percentage)<70)rv["bk"][code+"_Major"] = check
                    
                            }else{
                    
                                  if (parseInt(percentage) >= preventive_per){
                                    if(configP["client_name"] == "DentalDepot")rv["bk"][code+"_Basic"] = check
                                    else rv["bk"][code+"_Preventive"] = check
                                  }
                          
                                  if (parseInt(percentage) >= basic_per && parseInt(percentage) < preventive_per && parseInt(percentage) > major_per){
                                    rv["bk"][code+"_Basic"] = check              
                                  }
                          
                                  if (parseInt(percentage) < basic_per || parseInt(percentage) <= major_per){
                                    rv["bk"][code+"_Major"] = check
                                  }
                            }        
                        }
                    console.log(rv)
                    }
                  }
                  function SetFrequency(code, frequency) {
                    //console.log(code,frequency)
                    if (frequency_written_case.includes(code) && rv["bk"][code + "frequency"] == undefined) {
                        rv["bk"][code + "frequency"] = frequency
                    }
                    if (dup_frequency_written_case.includes(code) && rv["bk"]["DUP_" + code + "frequency"] == undefined) {
                        rv["bk"]["DUP_" + code + "frequency"] = frequency
                    }
                        if (patient_info_extract.includes('ReplacementClauseCrown') && rv["bk"]["ReplacementClauseCrown"] == undefined && ["D2950", "D2740"].includes(code)) {
                            rv["bk"]["ReplacementClauseCrown"] = frequency
                        }
                        if (patient_info_extract.includes('ReplacementClauseBridges') && rv["bk"]["ReplacementClauseBridges"] == undefined && ["D6245", "D5110"].includes(code)) {
                            rv["bk"]["ReplacementClauseBridges"] = frequency
                        }
                        if (patient_info_extract.includes('ReplacementClausePartialDentures') && rv["bk"]["ReplacementClausePartialDentures"] == undefined && ["D5211","D5225"].includes(code) ) {
                            rv["bk"]["ReplacementClausePartialDentures"] = frequency
                        }
                        if (patient_info_extract.includes('ReplacementClauseDentures') && rv["bk"]["ReplacementClauseDentures"] == undefined && code == "D5110") {
                            rv["bk"]["ReplacementClauseDentures"] = frequency
                        }
                        if (patient_info_extract.includes('ReplacementClauseProsthetic') && rv["bk"]["ReplacementClauseProsthetic"] == undefined && code == "D5110") {
                            rv["bk"]["ReplacementClauseProsthetic"] = frequency
                        }
                        if (patient_info_extract.includes('ReplacementClauseImplant') && rv["bk"]["ReplacementClauseImplant"] == undefined && code == "D6010") {
                            rv["bk"]["ReplacementClauseImplant"] = frequency
                        }
                        if (patient_info_extract.includes('ReplacementClauseFillings') && rv["bk"]["ReplacementClauseFillings"] == undefined && code == "D2391") {
                            rv["bk"]["ReplacementClauseFillings"] = frequency
                        }
                        if (patient_info_extract.includes('ReplacementClauseVeneers') && rv["bk"]["ReplacementClauseVeneers"] == undefined && code == "D2962"){
                            rv["bk"]["ReplacementClauseVeneers"] = frequency
                        }
                        if ( code == "D2740"&& configP["client_name"]=="Morrison Dental Group"){
                            rv["bk"]["D2950frequency"] = frequency
                        }
                        
                    
                  }
                  function SetAge(code, age_limit) {
                        if(patient_info_extract.includes("Orthodontics_AgeLimit") && code === "D8080")
                            rv["bk"]["Orthodontics_AgeLimit"] = age_limit
                        if(patient_info_extract.includes("Adult_Covered") && code === "D8080"){
                            let bk = parseInt(age_limit) > 18 ? `Adult_CoveredYES` : `Adult_CoveredNO`
                            rv["bk"][bk] = check
                  
                        }
                        if (age_limit && age_limit_cases.includes(code))
                            rv['bk'][code + "_AgeLimit"] = age_limit
                    
                  }
                  function SetDeductible(code, is_deductible) {
                        
                        if ( patient_info_extract.includes('Preventive_Deductibleapplies') && "Options" == "41"){
                            let bk = (is_deductible ) ? `Preventive_DeductibleappliesYES` : `Preventive_DeductibleappliesNO`
                            rv['bk'][bk] = check
                        }
                        if (patient_info_extract.includes('Isthedeductiblewaivedonpreventivecare') && "Options" == "41"){
                            let bk = (is_deductible ) ? `IsthedeductiblewaivedonpreventivecareNO` : `IsthedeductiblewaivedonpreventivecareYES`
                            rv['bk'][bk] = check
                        }
                        if (patient_info_extract.includes('Diagnostic_Deductibleapplies') && "Options" == "23"){
                            let bk = (is_deductible ) ? `Diagnostic_DeductibleappliesYES` : `Diagnostic_DeductibleappliesNO`
                            rv['bk'][bk] = check
                        }
                        if (patient_info_extract.includes('Periodontal_Deductibleapplies') && "Options" == "24"){
                            let bk = (is_deductible ) ? `Periodontal_DeductibleappliesYES` : `Periodontal_DeductibleappliesNO`
                            rv['bk'][bk] = check
                        }
                        if (patient_info_extract.includes('Endodontic_Deductibleapplies') && "Options" == "26"){
                            let bk = (is_deductible ) ? `Endodontic_DeductibleappliesYES` : `Endodontic_DeductibleappliesNO`
                            rv['bk'][bk] = check
                        }
                        if("Options" == "38" && patient_info_extract.includes("Orthodontics_Deductible")){
                            let table_deductible_ortho = Array.from(document.querySelectorAll(".well")).find(panel => panel.querySelector("legend")?.innerText.toUpperCase().includes(mode) && panel.querySelector("legend")?.innerText.toUpperCase().includes("DEDUCTIBLES"));
                            headers_ded_ortho = table_deductible_ortho != undefined ? Array.from(table_deductible_ortho.querySelectorAll("th")).filter(item => item?.innerText.trim() != "") : [];
                            rows_ded_ortho = table_deductible_ortho != undefined ? Array.from(table_deductible_ortho.querySelectorAll("tr:not(.headers)")).filter(item => item?.innerText.trim() != "") : [];
                            let deduc_ortho = "";
                            let index_type_deduc_ortho = headers_ded_ortho.findIndex(item => item?.innerText.toUpperCase().includes("TYPE"));
                            let index_coverage_deduc_ortho = headers_ded_ortho.findIndex(item => item?.innerText.toUpperCase().includes("COVERAGE"));
                            let index_amount_deduc_ortho = headers_ded_ortho.findIndex(item => item?.innerText.toUpperCase().includes("AMOUNT"));
                           
                            if(index_coverage_deduc_ortho != -1){
                                rows_ded_ortho = rows_ded_ortho.find(row => row.querySelectorAll("td")[index_coverage_deduc_ortho]?.innerText.includes("Individual") && 
                                (row.querySelectorAll("td")[index_type_deduc_ortho]?.innerText.includes("Ortho") || row.querySelectorAll("td")[index_type_deduc_ortho]?.innerText.includes("Dental")));
                                //console.log(rows_ded_ortho)
                              
                                if(index_amount_deduc_ortho != -1 && rows_ded_ortho != undefined){
                                    deduc_ortho = rows_ded_ortho != undefined ? rows_ded_ortho.querySelectorAll("td")[index_amount_deduc_ortho]?.innerText.trim() : undefined;
                                    console.log(deduc_ortho)
                                    if (patient_info_extract.includes("Orthodontics_Deductible") && deduc_ortho != undefined)
                                        rv["bk"]["Orthodontics_Deductible"] = deduc_ortho;
                                        
                                }        
                                
                            }
                
                        }
                        if (patient_info_extract.includes('Orthodontics_Deductibleapplies') && "Options" == "38"){
                            let bk = (is_deductible ) ? `Orthodontics_DeductibleappliesYES` : `Orthodontics_DeductibleappliesNO`
                            rv['bk'][bk] = check
                        }
                        if (patient_info_extract.includes('Basic_Deductibleapplies') && "Options" == '25'){
                            let bk = (is_deductible ) ? `Basic_DeductibleappliesYES` : `Basic_DeductibleappliesNO`
                            rv['bk'][bk] = check
                        }
                        if (patient_info_extract.includes('SimpleOralSX_Deductibleapplies') && "Options" === "40"){
                            let bk = (is_deductible ) ? `SimpleOralSX_DeductibleappliesYES` : `SimpleOralSX_DeductibleappliesNO`
                            rv['bk'][bk] = check
                        }
                        if (patient_info_extract.includes('OralSX_Deductibleapplies') && "Options" === "40"){
                            let bk = (is_deductible ) ? `OralSX_DeductibleappliesYES` : `OralSX_DeductibleappliesNO`
                            rv['bk'][bk] = check
                        }
                        if (patient_info_extract.includes('Major_Deductibleapplies') && "Options" == "36"){
                            let bk = (is_deductible ) ? `Major_DeductibleappliesYES` : `Major_DeductibleappliesNO`
                            rv['bk'][bk] = check
                        }
                        if (is_deductible )Options" == "41" && (patient_info_extract.includes("Deductibleappliesto") ||patient_info_extract.includes("Deductibleapplies")))
                                rv['bk']["DeductibleappliestoPREVENTIVE"] = check
                  
                            if("Options" == "25" && patient_info_extract.includes("Deductibleappliesto"))
                                rv['bk']["DeductibleappliestoBASIC"] = check
                  
                            if(("Options" == "36") && patient_info_extract.includes("Deductibleappliesto"))
                                rv['bk']["DeductibleappliestoMAJOR"] = check
                        }
                    
                  }
                  function SetAppliestoMax(code, is_to_max) {
                    if (patient_info_extract.includes('PreventiveappliestoMAX') && code == "D0120"){
                        let bk = (is_to_max) ? `PreventiveappliestoMAXYES` : `PreventiveappliestoMAXNO`
                        rv['bk'][bk] = check
                    }
                    if (is_to_max){
                        if (code == "D0120" && patient_info_extract.includes("AnnualMaximumapplies"))
                            rv['bk']["AnnualMaximumappliesPREVENTIVE"] = check
                  
                        if(code == "D2391" && patient_info_extract.includes("AnnualMaximumapplies"))
                            rv['bk']["AnnualMaximumappliesBASIC"] = check
                  
                        if((code == "D2740" || code == "D5110") && patient_info_extract.includes("AnnualMaximumapplies"))
                            rv['bk']["AnnualMaximumappliesMAJOR"] = check
                    }
                  
                  }
                  function SetSharedCase(code,codes_share){
                    
                    codes_share = codes_share.replace("Shares frequency with",'').split(",").map(code => {
                        if((/\D+\d4/gm).test(code)){
                            return code.match(/\D+\d4/gm)[0]
                        }
                    }).filter(code => code)
                    console.log(code,codes_share)
                    if(specific_share_case.includes(code)){
                        share_cases[specific_share_case.indexOf(code)].forEach(share_case =>{
                            codes_share.forEach(share_code_web=>{
                              console.warn(code,share_code_web,share_case)
                                if(share_code_web.trim() === share_case){
                                    rv["bk"][code.concat("_sharefreq".concat(share_case))] = check
                                }
                            })
                
                        })                
                
                    }
                  }
                  function convertYear(dateString) {
                    return dateString.replace(/\/(\d2)$/, (match, year) => {
                        return year < 30 ? `/20${year}` : `/19${year}`;
                    });
                }
                  function SetLastPerformed(code,last_performed){
                   // console.warn(last_performed)
                    if(last_performed && /\d2\/\d2\/\d2/.test(last_performed) && last_perform_cases.includes(code)){
                        last_performed = last_performed.match(/\d2\/\d2\/\d2/)[0]
                        if(last_performed.length > 0 && last_performed != "")
                            rv["bk"][code + "LastPerformed"] = convertYear(last_performed);
                    
                    
                    }
                    
                   
                  }
                  if(percentage_D7140 != "" && percentage_D7210 != "")configP["data"]["bookmarks"].includes("D7140_DifferentPercentage_D7210YES") && configP["data"]["bookmarks"].includes("D7140_DifferentPercentage_D7210NO")){
                        if(percentage_D7140 != percentage_D7210)
                            rv["bk"]["D7140_DifferentPercentage_D7210YES"] = check;
                        else
                            rv["bk"]["D7140_DifferentPercentage_D7210NO"] = check;
                    }
                  }
                  if(configP["data"]["bookmarks"].includes("D5731_Howlongafterdelivery")){
                    rv["bk"]["D5731_Howlongafterdelive"] = "-";
                  }
                  if(configP["data"]["bookmarks"].includes("D4341_Waitbetweenquads")){
                    rv["bk"]["D4341_Waitbetweenquads"] = "-";
                  }
                  if(configP["data"]["bookmarks"].includes("D9944_ForBruxismOnly")){
                    rv["bk"]["D9944_ForBruxismOnly"] = check;
                  }
                  
                  //console.log(not_covered_codes,rv,found_codes)
                console.log(rv)
                  return [rv,not_covered_codes]""",gsheet_columns, Options, found_codes, current_row, is_plan_hmo, configP, returned_values, bot_name, plan_medicare)
                returned_values = returned_values.decode()
                procedures_not_covered = returned_values[1]
                returned_values = returned_values[0]
                bot.scrap.load_url("{urlSearch}")
                bot.driver.execute_script(r"""                
                
                let button_vien_benefits = Array.from(document.querySelectorAll("a[id*='id']")).find(item => item.innerText.trim() != "" ? item.innerText.trim().includes("View Patient") : false);
                if(button_vien_benefits)
                	button_vien_benefits.click();""")
                bot.scrap.wait_for_object("present","id","longProcessPage",30)
                time.sleep(5)

