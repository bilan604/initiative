(() => {
    // A content (webpage innerHTML) retrieval template. Currently not requred in use.
    chrome.runtime.onMessage.addListener((obj, sender, response) => {
            console.log(obj, sender, response);    
            const {type, value, Id} = obj;
            
        }
    )
})