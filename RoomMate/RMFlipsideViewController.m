//
//  RMFlipsideViewController.m
//  RoomMate
//
//  Created by Alexander Kern on 7/12/13.
//  Copyright (c) 2013 Foobar Inc. All rights reserved.
//

#import "RMFlipsideViewController.h"

@interface RMFlipsideViewController ()

@end

@implementation RMFlipsideViewController

- (void)viewDidLoad
{
    [super viewDidLoad];
	// Do any additional setup after loading the view, typically from a nib.
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

#pragma mark - Actions

- (IBAction)done:(id)sender
{
    [self.delegate flipsideViewControllerDidFinish:self];
}

@end
