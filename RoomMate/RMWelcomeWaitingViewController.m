#import "RMWelcomeWaitingViewController.h"
#import "RMSettings.h"
#import "RMAppDelegate.h"

@implementation RMWelcomeWaitingViewController

- (void)viewDidAppear:(BOOL)animated {
    RMSettings *settings = [RMSettings settings];
    
    if (settings.groupID == nil) {
        RMAppDelegate *delegate = [[UIApplication sharedApplication] delegate];
        delegate.waiting = self;
    } else {
        [self finish];
    }
}

- (void)finish {
    [self performSegueWithIdentifier:@"finish" sender:self];
}

@end