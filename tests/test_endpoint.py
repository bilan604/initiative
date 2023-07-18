import json
import requests
from tests.static_info import *


"""
Default local test: Requires having input.csv in bilan604 folder
"""

def api_request(userId, operation, request_data):
    # Specified endpoint in main
    endpoint = "http://10.0.0.179:8000/api/"

    req_params = {
        "id": userId,
        "operation": operation,
        "request_data": json.dumps(request_data)
    }

    response = requests.get(endpoint, params=req_params)
    print("\nresponse:", response)
    
    return json.loads(response.text)

request_data = {
    "tablename": "input",
    "query": "How many years of Python programming experience do you have?"
}

response = api_request("bilan604", "search_datatable", request_data)
print("\nresponse:", response)


"""
Test for question extraction given page source and a lambda function:
"""

easy_apply_src = \
"""
<div class="ph5">
        <div class="pb4">
    <h3 class="t-16 t-bold">
      Additional Questions
    </h3>
<!----><!----><!----><!----><!----><!---->    <div class="jobs-easy-apply-form-section__grouping
        ">
              <div class="fb-dash-form-element jobs-easy-apply-form-element mt1" style="width:100%" tabindex="-1" aria-invalid="false" data-test-form-element="">
<!---->        

<div data-test-single-line-text-form-component="">
  <div id="ember1678" class="artdeco-text-input artdeco-text-input--type-text artdeco-text-input--color-default artdeco-text-input--state-required ember-view">  <div id="ember1679" class="artdeco-text-input--container ember-view">  <label for="single-line-text-form-component-formElement-urn-li-jobs-applyformcommon-easyApplyFormElement-3658969957-93027741-numeric" class="artdeco-text-input--label">How many years of work experience do you have with Data Pipelines?</label>
  <input class=" artdeco-text-input--input" id="single-line-text-form-component-formElement-urn-li-jobs-applyformcommon-easyApplyFormElement-3658969957-93027741-numeric" required="" aria-describedby="single-line-text-form-component-formElement-urn-li-jobs-applyformcommon-easyApplyFormElement-3658969957-93027741-numeric-error" type="text">
</div>
<!----><!----></div>

  <div id="single-line-text-form-component-formElement-urn-li-jobs-applyformcommon-easyApplyFormElement-3658969957-93027741-numeric-error">
<!----></div>
</div>
<!---->  </div>


    </div>
<!----><!---->    <div class="jobs-easy-apply-form-section__grouping
        ">
              <div class="fb-dash-form-element jobs-easy-apply-form-element mt4" style="width:100%" tabindex="-1" aria-invalid="false" data-test-form-element="">
<!---->        

<div data-test-single-line-text-form-component="">
  <div id="ember1680" class="artdeco-text-input artdeco-text-input--type-text artdeco-text-input--color-default artdeco-text-input--state-required ember-view">  <div id="ember1681" class="artdeco-text-input--container ember-view">  <label for="single-line-text-form-component-formElement-urn-li-jobs-applyformcommon-easyApplyFormElement-3658969957-93027733-numeric" class="artdeco-text-input--label">How many years of work experience do you have with Python (Programming Language)?</label>
  <input class=" artdeco-text-input--input" id="single-line-text-form-component-formElement-urn-li-jobs-applyformcommon-easyApplyFormElement-3658969957-93027733-numeric" required="" aria-describedby="single-line-text-form-component-formElement-urn-li-jobs-applyformcommon-easyApplyFormElement-3658969957-93027733-numeric-error" type="text">
</div>
<!----><!----></div>

  <div id="single-line-text-form-component-formElement-urn-li-jobs-applyformcommon-easyApplyFormElement-3658969957-93027733-numeric-error">
<!----></div>
</div>
<!---->  </div>


    </div>
<!----><!---->    <div class="jobs-easy-apply-form-section__grouping
        ">
              <div class="fb-dash-form-element jobs-easy-apply-form-element mt4" style="width:100%" tabindex="-1" aria-invalid="false" data-test-form-element="">
<!---->        

<div data-test-single-line-text-form-component="">
  <div id="ember1682" class="artdeco-text-input artdeco-text-input--type-text artdeco-text-input--color-default artdeco-text-input--state-required ember-view">  <div id="ember1683" class="artdeco-text-input--container ember-view">  <label for="single-line-text-form-component-formElement-urn-li-jobs-applyformcommon-easyApplyFormElement-3658969957-93027725-numeric" class="artdeco-text-input--label">How many years of work experience do you have with Shell Scripting?</label>
  <input class=" artdeco-text-input--input" id="single-line-text-form-component-formElement-urn-li-jobs-applyformcommon-easyApplyFormElement-3658969957-93027725-numeric" required="" aria-describedby="single-line-text-form-component-formElement-urn-li-jobs-applyformcommon-easyApplyFormElement-3658969957-93027725-numeric-error" type="text">
</div>
<!----><!----></div>

  <div id="single-line-text-form-component-formElement-urn-li-jobs-applyformcommon-easyApplyFormElement-3658969957-93027725-numeric-error">
<!----></div>
</div>
<!---->  </div>


    </div>
<!----><!---->    <div class="jobs-easy-apply-form-section__grouping
        ">
              <div class="fb-dash-form-element jobs-easy-apply-form-element mt4" style="width:100%" tabindex="-1" aria-invalid="false" data-test-form-element="">
<!---->        

<fieldset data-test-form-builder-radio-button-form-component="true" id="radio-button-form-component-formElement-urn-li-jobs-applyformcommon-easyApplyFormElement-3658969957-93027709-multipleChoice" aria-describedby="radio-button-form-component-formElement-urn-li-jobs-applyformcommon-easyApplyFormElement-3658969957-93027709-multipleChoice-error">
    <legend>
      <span data-test-form-builder-radio-button-form-component__title="" class="fb-dash-form-element__label
          fb-dash-form-element__label-title--is-required">
        <span aria-hidden="true"><!---->Are you comfortable working in a hybrid setting?<!----></span><span class="visually-hidden"><!---->Are you comfortable working in a hybrid setting?<!----></span>
      </span>

        <span class="visually-hidden" data-test-form-builder-radio-button-form-component__required="">
          Required
        </span>
    </legend>

      <div data-test-text-selectable-option="0" class="fb-text-selectable__option display-flex">
  <input data-test-text-selectable-option__input="Yes" id="urn:li:fsd_formElement:urn:li:jobs_applyformcommon_easyApplyFormElement:(3658969957,93027709,multipleChoice)-0" class="fb-form-element__checkbox" name="urn:li:fsd_formElement:urn:li:jobs_applyformcommon_easyApplyFormElement:(3658969957,93027709,multipleChoice)" aria-required="true" type="radio" value="Yes">
  <label data-test-text-selectable-option__label="Yes" for="urn:li:fsd_formElement:urn:li:jobs_applyformcommon_easyApplyFormElement:(3658969957,93027709,multipleChoice)-0" class="t-14">
    <!---->Yes<!---->
  </label>
</div>
      <div data-test-text-selectable-option="1" class="fb-text-selectable__option display-flex">
  <input data-test-text-selectable-option__input="No" id="urn:li:fsd_formElement:urn:li:jobs_applyformcommon_easyApplyFormElement:(3658969957,93027709,multipleChoice)-1" class="fb-form-element__checkbox" name="urn:li:fsd_formElement:urn:li:jobs_applyformcommon_easyApplyFormElement:(3658969957,93027709,multipleChoice)" aria-required="true" type="radio" value="No">
  <label data-test-text-selectable-option__label="No" for="urn:li:fsd_formElement:urn:li:jobs_applyformcommon_easyApplyFormElement:(3658969957,93027709,multipleChoice)-1" class="t-14">
    <!---->No<!---->
  </label>
</div>
</fieldset>

<div id="radio-button-form-component-formElement-urn-li-jobs-applyformcommon-easyApplyFormElement-3658969957-93027709-multipleChoice-error">
<!----></div>
<!---->  </div>


    </div>
<!----><!---->    <div class="jobs-easy-apply-form-section__grouping
        ">
              <div class="fb-dash-form-element jobs-easy-apply-form-element mt4" style="width:100%" tabindex="-1" aria-invalid="false" data-test-form-element="">
<!---->        

<fieldset data-test-form-builder-radio-button-form-component="true" id="radio-button-form-component-formElement-urn-li-jobs-applyformcommon-easyApplyFormElement-3658969957-93027717-multipleChoice" aria-describedby="radio-button-form-component-formElement-urn-li-jobs-applyformcommon-easyApplyFormElement-3658969957-93027717-multipleChoice-error">
    <legend>
      <span data-test-form-builder-radio-button-form-component__title="" class="fb-dash-form-element__label
          fb-dash-form-element__label-title--is-required">
        <span aria-hidden="true"><!---->Are you comfortable commuting to this job's location?<!----></span><span class="visually-hidden"><!---->Are you comfortable commuting to this job's location?<!----></span>
      </span>

        <span class="visually-hidden" data-test-form-builder-radio-button-form-component__required="">
          Required
        </span>
    </legend>

      <div data-test-text-selectable-option="0" class="fb-text-selectable__option display-flex">
  <input data-test-text-selectable-option__input="Yes" id="urn:li:fsd_formElement:urn:li:jobs_applyformcommon_easyApplyFormElement:(3658969957,93027717,multipleChoice)-0" class="fb-form-element__checkbox" name="urn:li:fsd_formElement:urn:li:jobs_applyformcommon_easyApplyFormElement:(3658969957,93027717,multipleChoice)" aria-required="true" type="radio" value="Yes">
  <label data-test-text-selectable-option__label="Yes" for="urn:li:fsd_formElement:urn:li:jobs_applyformcommon_easyApplyFormElement:(3658969957,93027717,multipleChoice)-0" class="t-14">
    <!---->Yes<!---->
  </label>
</div>
      <div data-test-text-selectable-option="1" class="fb-text-selectable__option display-flex">
  <input data-test-text-selectable-option__input="No" id="urn:li:fsd_formElement:urn:li:jobs_applyformcommon_easyApplyFormElement:(3658969957,93027717,multipleChoice)-1" class="fb-form-element__checkbox" name="urn:li:fsd_formElement:urn:li:jobs_applyformcommon_easyApplyFormElement:(3658969957,93027717,multipleChoice)" aria-required="true" type="radio" value="No">
  <label data-test-text-selectable-option__label="No" for="urn:li:fsd_formElement:urn:li:jobs_applyformcommon_easyApplyFormElement:(3658969957,93027717,multipleChoice)-1" class="t-14">
    <!---->No<!---->
  </label>
</div>
</fieldset>

<div id="radio-button-form-component-formElement-urn-li-jobs-applyformcommon-easyApplyFormElement-3658969957-93027717-multipleChoice-error">
<!----></div>
<!---->  </div>


    </div>
<!----><!---->    <div class="jobs-easy-apply-form-section__grouping
        ">
              <div class="fb-dash-form-element jobs-easy-apply-form-element mt4" style="width:100%" tabindex="-1" aria-invalid="false" data-test-form-element="">
<!---->        

<div data-test-text-entity-list-form-component="">
    <label for="text-entity-list-form-component-formElement-urn-li-jobs-applyformcommon-easyApplyFormElement-3658969957-93027757-multipleChoice" class="fb-dash-form-element__label
        fb-dash-form-element__label-title--is-required" data-test-text-entity-list-form-title="">
      <span aria-hidden="true"><!---->Do you have a U.S. Citizenship required to qualify for a DoD interim Secret (or higher) security clearance?<!----></span><span class="visually-hidden"><!---->Do you have a U.S. Citizenship required to qualify for a DoD interim Secret (or higher) security clearance?<!----></span>
    </label>

    <span class="visually-hidden" data-test-text-entity-list-form-required="">
      Required
    </span>

  <select id="text-entity-list-form-component-formElement-urn-li-jobs-applyformcommon-easyApplyFormElement-3658969957-93027757-multipleChoice" aria-describedby="text-entity-list-form-component-formElement-urn-li-jobs-applyformcommon-easyApplyFormElement-3658969957-93027757-multipleChoice-error" aria-required="true" required="" data-test-text-entity-list-form-select="">
      <option value="Select an option">
        Select an option
      </option>
      <option value="Yes">
        Yes
      </option>
      <option value="No">
        No
      </option>
  </select>

<!----></div>
<!---->  </div>


    </div>
<!----><!---->    <div class="jobs-easy-apply-form-section__grouping
        ">
              <div class="fb-dash-form-element jobs-easy-apply-form-element mt4" style="width:100%" tabindex="-1" aria-invalid="false" data-test-form-element="">
<!---->        

<div data-test-text-entity-list-form-component="">
    <label for="text-entity-list-form-component-formElement-urn-li-jobs-applyformcommon-easyApplyFormElement-3658969957-93027749-multipleChoice" class="fb-dash-form-element__label
        fb-dash-form-element__label-title--is-required" data-test-text-entity-list-form-title="">
      <span aria-hidden="true"><!---->Do you have at least 2+ years experience with any of the following: MATLAB, Embedded Multi-Threaded development, ARM microprocessors, or any deep learning, TensorFlow?<!----></span><span class="visually-hidden"><!---->Do you have at least 2+ years experience with any of the following: MATLAB, Embedded Multi-Threaded development, ARM microprocessors, or any deep learning, TensorFlow?<!----></span>
    </label>

    <span class="visually-hidden" data-test-text-entity-list-form-required="">
      Required
    </span>

  <select id="text-entity-list-form-component-formElement-urn-li-jobs-applyformcommon-easyApplyFormElement-3658969957-93027749-multipleChoice" aria-describedby="text-entity-list-form-component-formElement-urn-li-jobs-applyformcommon-easyApplyFormElement-3658969957-93027749-multipleChoice-error" aria-required="true" required="" data-test-text-entity-list-form-select="">
      <option value="Select an option">
        Select an option
      </option>
      <option value="Yes">
        Yes
      </option>
      <option value="No">
        No
      </option>
  </select>

<!----></div>
<!---->  </div>


    </div>
</div>

<!---->    </div>
"""

request_data = {
    "src": easy_apply_src,
    "rule": 'lambda x: "class" in x and "jobs-easy-apply-form-section__grouping" in x["class"]'
}

response = api_request("bilan604", "get_extracted_questions", request_data)

for r in response:
    print("Question:", r["question"])