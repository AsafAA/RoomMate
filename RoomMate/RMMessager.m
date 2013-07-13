#import "RMMessager.h"
#import "RMSettings.h"
#import "RMGroupID.h"

@implementation RMMessager

+ (RMMessager *)messager {
    static RMMessager *messager = nil;
    
    if (messager == nil) {
        messager = [[RMMessager alloc] init];
    }
    
    return messager;
}

- (void)showOnParent:(UIViewController *)parent {
    if ([MFMessageComposeViewController canSendText]) {
        MFMessageComposeViewController *controller = [[MFMessageComposeViewController alloc] init];

        controller.messageComposeDelegate = self;
        RMSettings *settings = [RMSettings settings];
        NSString *groupID = settings.groupID.string;
        controller.body = [NSString stringWithFormat:@"Let's be RoomMates! roommate://%@", groupID];
        
        [parent presentViewController:controller animated:YES completion:nil];
    }
}

- (void)messageComposeViewController:(MFMessageComposeViewController *)controller didFinishWithResult:(MessageComposeResult)result {
    [controller dismissViewControllerAnimated:YES completion:nil];
}

@end