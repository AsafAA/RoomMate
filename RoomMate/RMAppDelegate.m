#import "RMAppDelegate.h"
#import "RMSettings.h"
#import "RMWelcomeWaitingViewController.h"
#import "RMGroupID.h"

@implementation RMAppDelegate

- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions {
    RMSettings *settings = [RMSettings settings];
    [settings load];
    return YES;
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