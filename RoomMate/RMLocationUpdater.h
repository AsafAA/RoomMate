#import <Foundation/Foundation.h>
#import <CoreLocation/CoreLocation.h>

@interface RMLocationUpdater : NSObject <CLLocationManagerDelegate>

+ (RMLocationUpdater *)sharedUpdater;

- (void)start;

@end