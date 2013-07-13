#import "RMGroupID.h"

@implementation RMGroupID

- (id)init {
    self = [super init];
    
    if (self != nil) {
        self.string = [[NSUUID UUID] UUIDString];
    }
    
    return self;
}

- (id)initWithString:(NSString *)string {
    self = [super init];
    
    if (self != nil) {
        if ([[NSUUID alloc] initWithUUIDString:self.string] != nil) {
            self.string = string;
        } else {
            return nil;
        }
    }
    
    return self;
}

@end