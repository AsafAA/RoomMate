#import "RMWelcomeFinishViewController.h"
#import "RMSettings.h"

@implementation RMWelcomeFinishViewController

- (IBAction)dismissWelcome:(id)sender {
    RMSettings *settings = [RMSettings settings];
    [settings save];
    
    [self dismissViewControllerAnimated:YES completion:nil];
}

@end