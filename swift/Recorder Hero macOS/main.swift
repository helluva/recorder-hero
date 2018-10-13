//
//  main.swift
//  Recorder Hero macOS
//
//  Created by Cal Stephens on 10/13/18.
//  Copyright © 2018 Helluva. All rights reserved.
//

import Foundation

// This server is a super simple pass through layer that
// passes Peertalk messages from the iOS device to the
// Python gameplay app

let controller = PTServerController()

controller.didReceiveMessageBlock = { message in
    guard let message = message else {
        fatalError("Received empty message!")
    }
    
    print("MAIN.SWIFT:::::: \(message)")
}

controller.setup()

// start a run loop to keep the command line tool from dying
RunLoop.main.run()
