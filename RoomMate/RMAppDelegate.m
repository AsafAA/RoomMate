#import "RMAppDelegate.h"
#import "RMSettings.h"
#import "RMWelcomeWaitingViewController.h"
#import "RMGroupID.h"

@implementation RMAppDelegate

- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions {
    [[UIApplication sharedApplication] registerForRemoteNotificationTypes:UIRemoteNotificationTypeAlert];
    RMSettings *settings = [RMSettings settings];
    [settings load];
    return YES;
}

- (void)application:(UIApplication *)application didRegisterForRemoteNotificationsWithDeviceToken:(NSData *)deviceToken {
    RMSettings *settings = [RMSettings settings];
    const unsigned *tokenBytes = [deviceToken bytes];
    settings.deviceToken = [NSString stringWithFormat:@"%08x%08x%08x%08x%08x%08x%08x%08x", ntohl(tokenBytes[0]), ntohl(tokenBytes[1]), ntohl(tokenBytes[2]), ntohl(tokenBytes[3]), ntohl(tokenBytes[4]), ntohl(tokenBytes[5]), ntohl(tokenBytes[6]), ntohl(tokenBytes[7])];
}

- (BOOL)application:(UIApplication *)application openURL:(NSURL *)url sourceApplication:(NSString *)sourceApplication annotation:(id)annotation {
    if (url != nil) {
        NSString *groupID = [url host];
        
        RMSettings *settings = [RMSettings settings];
        settings.groupID = [[RMGroupID alloc] initWithString:groupID];
        [settings save];
        
        if (self.waiting != nil) {
            [self.waiting finish];
        }
    }
    
    return YES;
}

@end