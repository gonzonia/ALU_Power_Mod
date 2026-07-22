let SHUTDOWN_URL = "http:/<IP OF ALU>:8000/shutdown"; //Needs to be IP, HOSTNAME might not work
let SHUTDOWN_DELAY_MS = 30000; // adjust to whatever grace period you want
let pendingShutdownTimer = null;

function cutPower() {
  if (pendingShutdownTimer !== null) {
    Timer.clear(pendingShutdownTimer);
    pendingShutdownTimer = null;
  }
  console.log("Cutting Power");
  Shelly.call("Switch.Set", {id: 0, on: false});
}

function onWebhookResult(res, error_code, error_message) {
  if (error_code !== 0) {
    // Couldn't reach the ALU at all -- assume it's already off/unreachable
    // and cut power now instead of waiting out the grace period.
    console.log("Webhook call failed, Calling cutPower:", error_message);
    cutPower();
  }else{
    console.log("Response recieved",res);
  }
}

function onSwitchStatus(result) {
  if (result.output === true) {
    // Currently ON: notify ALU, then cut power after the delay regardless of its response
    console.log("Currently ON: notify ALU we want it to shutdown");
    Shelly.call("HTTP.POST", {
      url: SHUTDOWN_URL,
      body: "{\"action\":\"shutdown\",\"token\":\"<YOUR TOKEN HERE>\"}", 
      content_type: "application/json",
      timeout: 5
    }, onWebhookResult);

    if (pendingShutdownTimer !== null) {
    //  Timer.clear(pendingShutdownTimer);
    }
    
   pendingShutdownTimer = Timer.set(SHUTDOWN_DELAY_MS, false, cutPower);
   
  } else {
    // Currently OFF: turn on immediately, no delay needed
    console.log("Powered Off, Turning ALU on");
    Shelly.call("Switch.Set", {id: 0, on: true});
  }
}

function callReboot(result) {
  if (result.output === true) {
    // Currently ON: long press- notify ALU to reboot
    console.log("Currently ON: notify ALU we want it to reboot");
    Shelly.call("HTTP.POST", {
      url: SHUTDOWN_URL,
      body: "{\"action\":\"reboot\",\"token\":\"arcade3D\"}", 
      content_type: "application/json",
      timeout: 5
    }, onWebhookResult);
 }
} 
  
function onButtonEvent(event) {
  //Checking for button press on physical and virtual buttons
	if (event.component === "input:0" || event.component === "button:200"){
		if (event.info.event === "single_push") {
			console.log("Single Push Button Press Detected");
			Shelly.call("Switch.GetStatus", {id: 0}, onSwitchStatus);
		}
		if (event.info.event === "long_push") {
			console.log("Long Push Button Press Detected");
			Shelly.call("Switch.GetStatus", {id: 0}, callReboot);
       }  
	}
}

Shelly.addEventHandler(onButtonEvent);
