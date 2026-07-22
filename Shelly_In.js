let SHUTDOWN_DELAY_MS = 30000; // adjust to whatever grace period you want

let EXPECTED_TOKEN = "<YOUR TOKEN HERE>"; 

HTTPServer.registerEndpoint("shutdown", function(request, response) {
  if (request.method !== "POST") {
    console.log("Only POST allowed");
    response.code = 405;
    response.body = JSON.stringify({error: "Only POST allowed"});
    response.headers = [["Content-Type", "application/json"]];
    response.send();
    return;
  }
  
  // Parse JSON body
  let data;
  try {
    data = JSON.parse(request.body);
  } catch(e) {
    console.log("Invalid JSON");
    response.code = 400;
    response.body = JSON.stringify({error: "Invalid JSON"});
    response.headers = [["Content-Type", "application/json"]];
    response.send();
    return;
  }
  
  if (data.token != EXPECTED_TOKEN){
            console.log("Request received, Invalid Token");   
            response.code = 400;
            response.body = JSON.stringify({error: "Invalid Token"});
            response.headers = [["Content-Type", "application/json"]];
            response.send();
            return;
            }
  
  // Process the data
  if (data.action === "shutdown") {
	  console.log("Shutdown request recieved, shutting down in 30 seconds");
      Timer.set(SHUTDOWN_DELAY_MS, false, cutPower);
      response.body = JSON.stringify({"shutdown": "turning off in 30 seconds"});
      response.headers = [["Content-Type", "application/json"]];
      response.code = 200;
      response.send();
  } else {
    console.log("Unknown Action");
    response.code = 400;
    response.body = JSON.stringify({error: "Unknown action"});
    response.headers = [["Content-Type", "application/json"]];
    response.send();
  }
});

function cutPower() {
  console.log("Cutting Power");
  Shelly.call("Switch.Set", {id: 0, on: false});
}
