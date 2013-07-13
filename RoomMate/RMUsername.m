#import "RMUsername.h"

@implementation RMUsername

- (id)initWithString:(NSString *)string {
    self = [super init];
    
    if (self != nil) {
        if ([string isEqualToString:@""]) {
            return nil;
        } else {
            self.string = string;
        }
    }
    
    return self;
}

@end