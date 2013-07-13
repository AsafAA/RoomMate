#import <UIKit/UIKit.h>
#import <MessageUI/MessageUI.h>

@interface RMMessager : NSObject <MFMessageComposeViewControllerDelegate>

+ (RMMessager *)messager;
- (void)showOnParent:(UIViewController *)parent;

@end