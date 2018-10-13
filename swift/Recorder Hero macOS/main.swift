//
//  main.swift
//  Recorder Hero macOS
//
//  Created by Cal Stephens on 10/13/18.
//  Copyright © 2018 Helluva. All rights reserved.
//

import Foundation
import SwiftSocket

// This server is a super simple pass through layer that
// passes Peertalk messages from the iOS device to the
// Python gameplay app

// Peertalk talks to the iPhone over port 2345
// The socket to the python gameplay UI is over port 1457

let peertalkController = PTServerController()
let socket = TCPClient(address: "localhost", port: 1457)


// MARK: - configure the Socket client

switch socket.connect(timeout: 5) {
case .success:
    break
case .failure(let error):
    fatalError("Could not connect to the Python interface socket. \(error.localizedDescription)")
}


// MARK: - configure the Peertalk Server

peertalkController.didReceiveMessageBlock = { message in
    guard let message = message else {
        fatalError("Received empty message!")
    }
    
    print("Sending message: \(message)")
    let messageData = message.data(using: .utf8)!
    
    // create a three-byte header with the number of bytes expected in the message
    let byteCount = messageData.count
    
    let threeDigitByteCount: String
    switch "\(byteCount)".count {
    case 0: threeDigitByteCount = "000"
    case 1: threeDigitByteCount = "00\(byteCount)"
    case 2: threeDigitByteCount = "0\(byteCount)"
    case 3: threeDigitByteCount = "\(byteCount)"
    default: fatalError("Message longer than 999 bytes.")
    }
    
    let byteCountHeader = threeDigitByteCount.data(using: .utf8)!
    
    switch socket.send(data: byteCountHeader + messageData) {
    case .success:
        break
    case .failure(let error):
        fatalError("Could not send message over socket. \(error.localizedDescription)")
    }
}

peertalkController.setup()


// start a run loop to keep the command line tool from dying
RunLoop.main.run()
