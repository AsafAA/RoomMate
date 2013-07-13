#import "RMSettings.h"
#import "RMUsername.h"
#import "RMGroupID.h"
#import "RMAPI.h"

@implementation RMSettings

+ (RMSettings *)settings {
    static RMSettings *settings = nil;
    
    if (settings == nil) {
        settings = [[RMSettings alloc] init];
    }
    
    return settings;
}

- (BOOL)isInitialized {
    return self.username != nil && self.groupID != nil;
}

- (void)save {
    NSUserDefaults *defaults = [NSUserDefaults standardUserDefaults];
    [defaults setObject:self.username.string forKey:@"username"];
    [defaults setObject:self.groupID.string forKey:@"groupID"];
    [defaults setBool:self.privacyMode forKey:@"privacyMode"];
    [RMAPI updateUser];
}

- (void)load {
    NSUserDefaults *defaults = [NSUserDefaults standardUserDefaults];
    self.username = [[RMUsername alloc] initWithString:[defaults objectForKey:@"username"]];
    self.groupID = [[RMGroupID alloc] initWithString:[defaults objectForKey:@"groupID"]];
    self.privacyMode = [defaults boolForKey:@"privacyMode"];
}

@end