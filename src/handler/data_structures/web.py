
class Company(object):

    def __init__(self, company_profile_url):
        self.company_profile_url = company_profile_url
        self.num_employees_matching_keyword_engineer = 0
        self.num_usa_profiles_matching_keyword_engineer = 0
        self.total_employees = 0
        self.total_eng_headcount = 0
        self.city = ""
        self.visit_website_url = ""
        self.linkedin_tag_line = ""
        
        self.company_image_url = ""
        
        self.engineering_6m_pct_growth = ""
        self.engineering_1y_pct_growth = ""
        self.overall_6m_pct_growth = ""
        self.overall_1y_pct_growth = ""
        self.overall_2y_pct_growth = ""

    def to_dict(self):
        dictionary = {}
        dictionary['company_profile_url'] = self.company_profile_url
        dictionary['num_employees_matching_keyword_engineer'] = self.num_employees_matching_keyword_engineer
        dictionary['num_usa_profiles_matching_keyword_engineer'] = self.num_usa_profiles_matching_keyword_engineer
        dictionary['total_employees'] = self.total_employees
        dictionary['total_eng_headcount'] = self.total_eng_headcount
        dictionary['city'] = self.city
        dictionary['visit_website_url'] = self.visit_website_url
        dictionary['linkedin_tag_line'] = self.linkedin_tag_line

        dictionary['company_image_url'] = self.company_image_url

        dictionary['engineering_6m_pct_growth'] = self.engineering_6m_pct_growth
        dictionary['engineering_1y_pct_growth'] = self.engineering_1y_pct_growth
        dictionary['overall_6m_pct_growth'] = self.overall_6m_pct_growth
        dictionary['overall_1y_pct_growth'] = self.overall_1y_pct_growth
        dictionary['overall_2y_pct_growth'] = self.overall_2y_pct_growth
        return dictionary