#import <UIKit/UIKit.h>

@class RMUser;
@class RMWelcomeWaitingViewController;

@interface RMAppDelegate : UIResponder <UIApplicationDelegate>

@property (strong, nonatomic) UIWindow *window;
@property (weak, nonatomic) RMWelcomeWaitingViewController *waiting;

@end