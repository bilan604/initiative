// The minimum number of triggers for this extension to trigger
const INPUT_THRESHOLD = 4;


/**
 * 
 * @param {string} src: The innerHTML for the webpage
 * @returns The innerHTML for the body element of the webpage
 */
function getBody(src) {
    let bodyStart = src.indexOf("<body");
    let bodyEnd = src.indexOf("</body>");
    let bodyContent = src.slice(bodyStart, bodyEnd + 7);
    return bodyContent;
}

/**
 * 
 * @param {string} src: The innerHTML for the webpage
 * @returns Whether to perform an operation on the webpage
 */
function determineTrigger(src) {
    let target = "<input";
    let count = 0;
    for (let i=0; i<src.length-target.length+1; i++) {
        if (src.substring(i, i+target.length) === target) {
            count++;
        }
    }

    if (count >= INPUT_THRESHOLD) {
        return true;
    }
    return false;
}


async function fetchData(data, url) {
    let fetchResponse = fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    }).then(response => response.json());

    return fetchResponse;
}


/**
 * 
 * @param {string} src: The innerHTML of the webpage
 * @returns 
 */
async function handleOperation(userId, dataOperation, requestData) {
    if (requestData === undefined || requestData === null) {
        console.log("requestData provided invalid:", requestData);
        return "requestData not valid"
    }
    if (typeof dataOperation !== 'string' || dataOperation.length === 0) {
        console.log("Invalid operation specified:", dataOperation);
        return 'Invalid operation specified';
    }
    if (dataOperation === "Question-Answer-Fast" || dataOperation === "Question-Answer-LLM") {
        requestData = getBody(requestData);
    }

    let data = {
        id: userId,
        operation: dataOperation,
        requestData: requestData,
    };
    let apiEndpoint = 'http://10.0.0.179:8000/api/';

    let endpointResponse = await fetchData(data, apiEndpoint);
    return endpointResponse;

}


// This function is executed once and adds a listener. The properties of the chrome extension
// are defined in the following code cell block. The configuration is specified in the manifest.json file.
chrome.runtime.onInstalled.addListener(() => {
    console.log("chrome.runtime.onInstalled");

    chrome.tabs.onUpdated.addListener(async (tabId, tab) => {
        console.log("Tab Updated");
        
        if (tab.status === "complete") {
            // Call the endpoint
            chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
                if (tabs.length > 0) {
                    const tab = tabs[0];
                    chrome.tabs.executeScript(tab.id, { code: 'document.documentElement.innerHTML' }, async (result) => {
                        if (chrome.runtime.lastError) {
                            console.log(chrome.runtime.lastError);
                        } else {
                            let src = result[0];

                            if (determineTrigger(src)) {
                                let id = "testId";
                                let requestData1 = {
                                    html_content: src
                                };
                                let resp1 = await handleOperation(id, "get_question_answer_prompts", requestData1);
                                console.log("The prompts:", resp1);

                                let requestData2 = {
                                    prompts: resp1,
                                    api_key: "[GPT_4_API_KEY]"
                                };
                                let resp2 = await handleOperation(id, "get_question_answer_prompt_responses", requestData2);
                                console.log("The question-answers:", resp2);

                                let requestData3 = {
                                    qas: resp2
                                };
                                let resp3 = await handleOperation(id, "answer_input_questions", requestData3);
                                console.log("question-answers filtered and answered by matched questions:", resp3);

                            }
                            
                        }
                    });
                }
            });
        
        }
    
        
    });

  });
