import subprocess
import json
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt

def get_company_info(company_no):
    """
    Retrieves information about a company from Companies House.
    Args:
        company_no (str): Registered company number.
    Returns:
        Information Companies House holds on the company.
    """
    in_ = 'curl -s -X GET -u yLwgnyHvwlYxkbOBAoLEwsaEfVQ_a7kAuCUTNtSt: https://api.companieshouse.gov.uk/company/{}/officers?q=Officers&items_per_page=100&start_index=0'.format(company_no).split()

    out = subprocess.check_output(in_)
    res = json.loads(out.decode('utf8'))
    ret = res['items']
   
    return ret


def get_associated_companies_info_by_company(company_no, companies_recorded, depth):
    """
    Finds information about all companies associated through officers with the starting company.

    Args:
        company_no (str):  The company number we want to search associated companies with.
        depth (int): The depth of search in the graph of companies.
        companies_record (list): A list of the company_no of any companies information that has already been recorded

    Returns:
        A list of information about all associated companies up to the given depth.
    """
   
    if company_no in companies_recorded:
        return []
    
    ret = []
    company_info = get_company_info(company_no)
    new_depth = depth - 1
    
    for i in company_info:
        url_patch = i['links']['officer']['appointments']
        bash_command = 'curl -s -X GET -u yLwgnyHvwlYxkbOBAoLEwsaEfVQ_a7kAuCUTNtSt: https://api.companieshouse.gov.uk{}'.format(url_patch)
        url =  bash_command.split()
        check = subprocess.check_output(url)
        info = json.loads(check.decode('utf8'))['items']
        
        ret.append(info)
        companies_recorded = companies_recorded + [x['appointed_to']['company_number'] for x in info]
        
        if new_depth > 0:
            for _ in range(new_depth):
                for i in companies_recorded:
                    ret.append(get_associated_companies_info_by_company(i, companies_recorded, new_depth))
            
            
    
    return ret



def generate_officer_appointment_dict(info_list):
    """
    Generates a dictionary of each officers company affiliations.

    Args:
        
        info_list (list):A list of information about all associated companies up to the given depth.

    Returns:
        A dictionary of officers and their appointments.
    """
   
    
    info_list = [x for x in info_list if x != []]
    officer_company_dict = {}
    for i in info_list:
        companies = []
        for j in i:
            companies.append(j['appointed_to']['company_name'])
    
        officer_company_dict[i[0]['name']] = companies
            
    return officer_company_dict

def visusalise_appointments(officer_appointments):
    """
    Generates a colourmap visualising officers and their appointments.

    Args:
        
        officer_appointments (dictionary):A dictionary of officers and their appointments.

    Returns:
        A colourmap showing officers and companies they are appointed to.
    """
    
    
    all_company_names = []
    for i in officer_appointments.values():
        all_company_names += [x for x in i]

    officer_appointment_df = pd.DataFrame(columns=officer_appointments.keys(), index=list(set(all_company_names)))
    for i in officer_appointment_df.columns:
        officer_appointment_df[i] = [1 if j in officer_appointments[i] else 0 for j in officer_appointment_df.index]
    
    plt.title
    plt.figure(num=None, figsize=(len(officer_appointment_df.columns),int(len(all_company_names)*0.6)), dpi=300)
    sn.heatmap(officer_appointment_df, cmap='YlGnBu', linewidths=.5, linecolor='royalblue', cbar_kws={'shrink':0.5, 'ticks':[0,1], 'label': '0 = Not Appointed \n1 = Appointed'})
    plt.title
    plt.savefig('Associated Company Visualisation.png', dpi=600, bbox_inches='tight', orientation='landscape')
    # plt.show()
    
    
    return officer_appointment_df

if __name__ == '__main__':
    company_number = str(input('Enter company number:'))
    depth_no = int(input('Enter depth:'))
    output_1 = get_associated_companies_info_by_company(company_number, [], depth_no)
    dict_ = generate_officer_appointment_dict(output_1)
    visusalise_appointments(dict_)



