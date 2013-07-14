#import <UIKit/UIKit.h>

@class RMUsername;
@class RMGroupID;

@interface RMSettings : UIViewController

@property (strong, nonatomic) RMUsername *username;
@property (strong, nonatomic) RMGroupID *groupID;
@property (assign, nonatomic) BOOL privacyMode;
@property (strong, atomic) NSString *deviceToken;

+ (RMSettings *)settings;

- (BOOL)isInitialized;
- (void)save;
- (void)load;

@end