#import <Foundation/Foundation.h>
#import <CoreLocation/CoreLocation.h>

@interface RMAPI : NSObject

+ (void)updateUser;
+ (void)updateLocation:(CLLocation *)location;

@end