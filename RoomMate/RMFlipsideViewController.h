//
//  RMFlipsideViewController.h
//  RoomMate
//
//  Created by Alexander Kern on 7/12/13.
//  Copyright (c) 2013 Foobar Inc. All rights reserved.
//

#import <UIKit/UIKit.h>

@class RMFlipsideViewController;

@protocol RMFlipsideViewControllerDelegate
- (void)flipsideViewControllerDidFinish:(RMFlipsideViewController *)controller;
@end

@interface RMFlipsideViewController : UIViewController

@property (weak, nonatomic) id <RMFlipsideViewControllerDelegate> delegate;

- (IBAction)done:(id)sender;

@end
