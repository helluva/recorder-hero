//
//  AppDelegate.swift
//  Recorder Hero macOS Passthrough
//
//  Created by Cal Stephens on 10/13/18.
//  Copyright © 2018 Helluva. All rights reserved.
//

import Cocoa
import SwiftSocket


// This server is a super simple pass through layer that
// passes Peertalk messages from the iOS device to the Python gameplay app.


@NSApplicationMain
class AppDelegate: NSObject, NSApplicationDelegate {

    @IBOutlet weak var window: NSWindow!


    func applicationDidFinishLaunching(_ aNotification: Notification) {
        
        // run headless
        window.orderOut(self)
        
        // Peertalk talks to the iPhone over port 2345
        // The socket to the python gameplay UI is over a port specified by the Python app.
        // This app is launched by the Python app as a Command Line helper.
        let peertalkController = PTServerController()
        
        guard CommandLine.arguments.count >= 3,
            CommandLine.arguments[1] == "-p",
            let port = Int32(CommandLine.arguments[2]) else
        {
            fatalError("Incorrect usage. Launch with `-p [port].`")
        }
        
        
        let socket = TCPClient(address: "localhost", port: port)
        
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
        
    }


}

