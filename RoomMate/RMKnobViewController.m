#import "RMKnobViewController.h"
#import "RMLocationUpdater.h"
#import "RMSettings.h"

@implementation RMKnobViewController

- (IBAction)privacyModeChanged:(id)sender {
    RMSettings *settings = [RMSettings settings];
    settings.privacyMode = self.privacyModeSwitch.on;
    [settings save];
}

- (void)viewDidLoad {
    RMSettings *settings = [RMSettings settings];
    self.privacyModeSwitch.on = settings.privacyMode;
    
    [[RMLocationUpdater sharedUpdater] start];
}

- (void)viewDidAppear:(BOOL)animated {
    RMSettings *settings = [RMSettings settings];
    
    if (![settings isInitialized]) {
        UINavigationController *controller = [self.storyboard instantiateViewControllerWithIdentifier:@"Welcome"];
        [self presentViewController:controller animated:YES completion:nil];
    }
}

@end