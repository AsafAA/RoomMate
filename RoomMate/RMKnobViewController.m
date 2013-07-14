#import "RMKnobViewController.h"
#import "RMLocationUpdater.h"
#import "RMSettings.h"

@implementation RMKnobViewController

- (IBAction)buttonClicked:(id)sender {
    RMSettings *settings = [RMSettings settings];
    settings.privacyMode = !settings.privacyMode;
    self.button.selected = settings.privacyMode;
    [settings save];
}

- (IBAction)fake1:(id)sender {
    [NSTimer scheduledTimerWithTimeInterval:5.0 target:self selector:@selector(fakeMessage1) userInfo:nil repeats:NO];
}

- (IBAction)fake2:(id)sender {
    [NSTimer scheduledTimerWithTimeInterval:5.0 target:self selector:@selector(fakeMessage2) userInfo:nil repeats:NO];
}

- (void)fakeMessage1 {
    UIAlertView *alert = [[UIAlertView alloc] initWithTitle:@"RoomMate" message:@"James is approaching!" delegate:nil cancelButtonTitle:@"Ok" otherButtonTitles:nil];
    [alert show];
}

- (void)fakeMessage2 {
    UIAlertView *alert = [[UIAlertView alloc] initWithTitle:@"RoomMate" message:@"Asaf is using the room right now! Don't come in just yet." delegate:nil cancelButtonTitle:@"Ok" otherButtonTitles:nil];
    [alert show];
}

- (void)viewDidLoad {
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