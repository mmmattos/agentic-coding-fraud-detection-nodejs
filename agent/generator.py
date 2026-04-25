
import os

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)

def generate_system(plan, base):

    write(f"{base}/package.json", '''{
  "name": "fraud-system",
  "version": "1.0.0",
  "dependencies": {
    "@grpc/grpc-js": "^1.8.0",
    "@grpc/proto-loader": "^0.7.0"
  }
}''')

    write(f"{base}/proto/fraud.proto", '''syntax = "proto3";

service TransactionService {
  rpc Stream (Empty) returns (Transaction);
}

service DecisionService {
  rpc Decide (Transaction) returns (Decision);
}

message Empty {}

message Transaction {
  string id = 1;
  double amount = 2;
}

message Decision {
  string action = 1;
}''')

    write(f"{base}/services/transaction_server.js", '''const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');

const packageDef = protoLoader.loadSync(__dirname + '/../proto/fraud.proto');
const grpcObject = grpc.loadPackageDefinition(packageDef);

function stream(call, callback) {
  const txn = {
    id: Math.floor(Math.random() * 10000).toString(),
    amount: [10,50,10000][Math.floor(Math.random()*3)]
  };
  callback(null, txn);
}

function start() {
  const server = new grpc.Server();
  server.addService(grpcObject.TransactionService.service, { Stream: stream });

  server.bindAsync('0.0.0.0:50051', grpc.ServerCredentials.createInsecure(), () => {
    console.log("Transaction service running 50051");
  });
}

module.exports = { start };''')

    write(f"{base}/services/decision_server.js", '''const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');

const packageDef = protoLoader.loadSync(__dirname + '/../proto/fraud.proto');
const grpcObject = grpc.loadPackageDefinition(packageDef);

function decide(call, callback) {
  const txn = call.request;

  let action = "APPROVE";
  if (txn.amount > 5000) action = "BLOCK";

  callback(null, { action });
}

function start() {
  const server = new grpc.Server();
  server.addService(grpcObject.DecisionService.service, { Decide: decide });

  server.bindAsync('0.0.0.0:50052', grpc.ServerCredentials.createInsecure(), () => {
    console.log("Decision service running 50052");
  });
}

module.exports = { start };''')

    write(f"{base}/client.js", '''const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');

const { start: startTxn } = require('./services/transaction_server');
const { start: startDecision } = require('./services/decision_server');

startTxn();
startDecision();

const packageDef = protoLoader.loadSync(__dirname + '/proto/fraud.proto');
const grpcObject = grpc.loadPackageDefinition(packageDef);

const txnClient = new grpcObject.TransactionService(
  'localhost:50051',
  grpc.credentials.createInsecure()
);

const decisionClient = new grpcObject.DecisionService(
  'localhost:50052',
  grpc.credentials.createInsecure()
);

setInterval(() => {
  txnClient.Stream({}, (err, txn) => {
    if (err) return console.error(err);

    decisionClient.Decide(txn, (err, res) => {
      if (err) return console.error(err);
      console.log(`${txn.amount} → ${res.action}`);
    });
  });
}, 1000);
''')
