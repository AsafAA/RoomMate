#import <MessageUI/MessageUI.h>
#import "RMWelcomeGroupViewController.h"
#import "RMMessager.h"
#import "RMSettings.h"
#import "RMGroupID.h"

@implementation RMWelcomeGroupViewController

- (IBAction)createGroup:(id)sender {
    RMMessager *messager = [RMMessager messager];
    [messager showOnParent:self];
}

@end