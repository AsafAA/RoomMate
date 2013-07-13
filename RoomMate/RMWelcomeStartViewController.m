#import "RMWelcomeStartViewController.h"
#import "RMSettings.h"
#import "RMUsername.h"

@implementation RMWelcomeStartViewController

- (IBAction)nameFieldChanged:(id)sender {
    RMSettings *settings = [RMSettings settings];
    NSString *name = self.nameField.text;
    
    if ([name isEqualToString:@""]) {
        self.nextButton.enabled = NO;
    } else {
        self.nextButton.enabled = YES;
        settings.username = [[RMUsername alloc] initWithString:name];
    }
}

- (IBAction)dismissKeyboard:(id)sender {
    [sender resignFirstResponder];
}

@end