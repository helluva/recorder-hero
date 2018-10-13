//
//  ViewController.swift
//  Recorder Hero
//
//  Created by Cal Stephens on 10/13/18.
//  Copyright © 2018 Helluva. All rights reserved.
//

import UIKit

class ViewController: UIViewController {

    let connectionIndicator = UIView(frame: CGRect(x: 15, y: 10, width: 60, height: 25))
    
    let recorderButtons = [
        RecorderButton(),
        RecorderButton(),
        RecorderButton(),
        RecorderButton(),
        RecorderButton(),
        RecorderButton(),
        RecorderButton()
    ]
    
    /// x is relative to center, y is relative to top
    let recorderButtonPositions = [
        CGPoint(x: -10, y: 100),
        CGPoint(x: -10, y: 200),
        CGPoint(x: -3,  y: 310),
        CGPoint(x: -10, y: 415),
        CGPoint(x: -10, y: 525),
        CGPoint(x: -8,  y: 610),
        CGPoint(x: -25, y: 710)]
    
    
    override func viewDidLoad() {
        NotificationCenter.default.addObserver(self,
            selector: #selector(updateConnectionIndicator),
            name: .peertalkClientConnectionEstablishedNotification,
            object: nil)
        
        NotificationCenter.default.addObserver(self,
            selector: #selector(updateConnectionIndicator),
            name: .peertalkClientConnectionLostNotification,
            object: nil)
        
        view.addSubview(connectionIndicator)
        connectionIndicator.layer.cornerRadius = connectionIndicator.frame.height / 2
        connectionIndicator.layer.masksToBounds = true
        updateConnectionIndicator(nil)
    }
    
    override func viewDidAppear(_ animated: Bool) {
        // set up the recorder buttons
        for (recorderButton, position) in zip(recorderButtons, recorderButtonPositions) {
            view.addSubview(recorderButton)
            recorderButton.frame.origin = CGPoint(
                x: (view.frame.width / 2) - (recorderButton.frame.width / 2) + position.x,
                y: position.y - (recorderButton.frame.height / 2))
            
            recorderButton.stateUpdatedHandler = self.recorderButtonStateDidUpdate(_:)
        }
    }
    
    
    private func recorderButtonStateDidUpdate(_ recorderButton: RecorderButton) {
        let stateVector = recorderButtons.map { $0.pressed ? "1" : "0" }.reduce("", +)
        PeertalkClient.shared.sendMessage(stateVector)
    }
    
    @objc func updateConnectionIndicator(_ notification: NSNotification?) {
        UIView.transition(with: connectionIndicator, duration: 0.3, options: .transitionCrossDissolve, animations: {
            self.connectionIndicator.backgroundColor = PeertalkClient.shared.isConnected ? #colorLiteral(red: 0.7366020005, green: 0.9768045545, blue: 0.7366020005, alpha: 1) : #colorLiteral(red: 1, green: 0.6383535342, blue: 0.5749678938, alpha: 1)
        }, completion: nil)
    }

}

