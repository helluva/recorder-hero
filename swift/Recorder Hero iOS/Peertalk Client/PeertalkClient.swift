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
    
    private let controller = PTClientController()
    
    private override init() {
        super.init()
    }
    
    
    func connectToServer() {
        controller.setup()
    }
    
}

