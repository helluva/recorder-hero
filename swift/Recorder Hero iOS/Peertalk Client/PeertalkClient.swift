//
//  PeertalkClient.swift
//  Recorder Hero
//
//  Created by Cal Stephens on 10/13/18.
//  Copyright © 2018 Helluva. All rights reserved.
//

import Foundation


// MARK: - Peertalk Interface

class PeertalkClient: NSObject {
    
    
    // MARK: Singleton
    
    static let shared = PeertalkClient()
    
    
    // MARK: Instance
    
    var isConnected = false
    private let controller = PTClientController()
    
    private override init() {
        super.init()
    }
    
    
    func connectToServer() {
        controller.setup()
        
        controller.connectionEstablishedBlock = { [weak self] in
            self?.isConnected = true
            NotificationCenter.default.post(name: .peertalkClientConnectionEstablishedNotification, object: nil)
        }
        
        controller.connectionLostBlock = { [weak self] in
            self?.isConnected = false
            NotificationCenter.default.post(name: .peertalkClientConnectionLostNotification, object: nil)
        }
    }
    
    func sendMessage(_ message: String) {
        controller.sendMessage(message)
    }
    
}


// MARK: Notifications

extension NSNotification.Name {
    
    static let peertalkClientConnectionEstablishedNotification = NSNotification.Name("peertalkClientConnectionEstablishedNotification")
    
    static let peertalkClientConnectionLostNotification = NSNotification.Name("peertalkClientConnectionLostNotification")
    
}
