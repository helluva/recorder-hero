//
//  RecorderButton.swift
//  Recorder Hero iOS
//
//  Created by Cal Stephens on 10/13/18.
//  Copyright © 2018 Helluva. All rights reserved.
//

import UIKit

class RecorderButton: UIView {
    
    private static let pressedColor = UIColor(white: 0, alpha: 0.65)
    private static let unpressedColor = UIColor(white: 0, alpha: 0.3)
    
    var pressed = false {
        willSet {
            if newValue != pressed {
                UIImpactFeedbackGenerator(style: .heavy).impactOccurred()
            }
        }
        didSet {
            stateUpdatedHandler?(self)
            
            backgroundColor = (pressed)
                ? RecorderButton.pressedColor
                : RecorderButton.unpressedColor
        }
    }
    
    var stateUpdatedHandler: ((RecorderButton) -> Void)?
    
    
    init() {
        super.init(frame: CGRect(origin: .zero, size: CGSize(width: 75, height: 75)))
        backgroundColor = RecorderButton.unpressedColor
        layer.cornerRadius = frame.size.width / 2
        layer.masksToBounds = true
    }
    
    required init?(coder aDecoder: NSCoder) {
        fatalError("Not implemented.")
    }
    
    
    override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent?) {
        pressed = true
    }
    
    override func touchesEnded(_ touches: Set<UITouch>, with event: UIEvent?) {
        pressed = false
    }
    
    override func touchesCancelled(_ touches: Set<UITouch>, with event: UIEvent?) {
        pressed = false
    }
    
}
