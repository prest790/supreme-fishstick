// Import required modules
const { spawn } = require('child_process');
const fs = require('fs');
const readline = require('readline');

// Function to execute the Python script
const childPython = spawn('python', ['--version']);
//const childPython = spawn('python', ['codespace.py']);
//const childPython = spawn('python', ['codespace.py', 'OyeKool']);

function runPythonScript() {
    const pythonProcess = spawn('python', ['python_scripts/generate.py']);

    // Create a write stream to save the output to CSV
    const outputStream = fs.createWriteStream('output/generated_addresses.csv');

    // Create a read stream to check for matches in known_addresses.txt
    const inputStream = readline.createInterface({
    input: fs.createReadStream('python_scripts/known_addresses.txt'),
    output: process.stdout,
    console: false
});

    // Set up event listeners for the Python script output
    pythonProcess.stdout.on('data', (data) => {
    console.log(`stdout: ${data}`);
    outputStream.write(data);
    });

pythonProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
});

pythonProcess.on('close', (code) => {
    console.log(`child process exited with code ${code}`);
    outputStream.end();
});


    // Check for matches in known_addresses.txt
    function checkForMatches(addresses) {
        const knownAddresses = fs.readFileSync('other_addresses.txt', 'utf8').split('\n');
        const matches = [];
        for (let i = 0; i < addresses.length; i++) {
        if (knownAddresses.includes(addresses[i])) {
            matches.push(addresses[i]);
        }
        }
    return matches;
}
pythonProcess.stderr.on('data', (data) => {
    console.error(`Python Error: ${data}`);
});

  // Event listener for script completion
pythonProcess.on('close', () => {
    console.log(`Generation completed! Total addresses generated: ${count}`);
    outputStream.end();
});
}

// Function to stop the script when a match is found
function stopScript() {
process.exit(0);
}

// Run the Python script and start address generation
runPythonScript();
