#import "RMSettingsViewController.h"
#import "RMSettings.h"
#import "RMMessager.h"
#import "RMGroupID.h"
#import "RMUsername.h"

@implementation RMSettingsViewController

- (IBAction)done:(id)sender {
    RMSettings *settings = [RMSettings settings];
    [settings save];

    [self dismissViewControllerAnimated:YES completion:nil];
}

- (IBAction)dismissKeyboard:(id)sender {
    [sender resignFirstResponder];
    [self saveName];
}

- (IBAction)newGroup:(id)sender {
    RMSettings *settings = [RMSettings settings];
    settings.groupID = [[RMGroupID alloc] init];

    [self addRoommates:self];
}

- (IBAction)addRoommates:(id)sender {
	RMMessager *messager = [RMMessager messager];
    [messager showOnParent:self];
}

- (void)viewWillAppear:(BOOL)animated {
    RMSettings *settings = [RMSettings settings];
    self.nameField.text = settings.username.string;
}

- (void)viewWillDisappear:(BOOL)animated {
    [self saveName];
}

- (void)saveName {
    RMSettings *settings = [RMSettings settings];
    NSString *name = self.nameField.text;
    
    if ([name isEqualToString:@""]) {
        self.nameField.text = settings.username.string;
    } else {
        settings.username = [[RMUsername alloc] initWithString:name];
    }
}

@end