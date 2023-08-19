class BardInstructor(WebHelper):

    def sign_in(self):
        button = get_element(self.driver.page_source, "button", lambda x: "sign in" in x.strip().lower(), lambda x: True)
        print("SIGN IN ", button)
        xpath = get_xpath_by_element(button)
        self.click(xpath)

    def send(self):
        btns = BeautifulSoup(self.driver.page_source).find_all("button", {"id": "send-button"})
        btns = list(map(str, btns))
        # be null cuz dash?
        print(btns, len(btns))
        

    def write_prompt(self, message):
        text_areas = BeautifulSoup(self.driver.page_source).find_all("textarea", {"id": "mat-input-0"})
        text_areas = list(map(str, text_areas))
        print("text_areas", text_areas, len(text_areas))
        if text_areas:
            xpath = get_xpath_by_element(text_areas[0])
            self.write(xpath, message)

    def get_response(self):
        
        response = ""
        return "PLC"

    def query(self, message):
        self.write_prompt(message)
        self.send()
        # message most likely not needed
        response = self.get_response()
        return response