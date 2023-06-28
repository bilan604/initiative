(()=>{
    // This is a runtime script tempalte
    chrome.runtime.onMessage.addListener((obj, sender, response) => {
        console.log("script ran");
    });
    
})