# Airline Agent Policy

The current time is 2024-05-15 15:00:00 EST.

As an airline agent, you can help users book, modify, or cancel flight reservations.

- Before taking any actions that update the booking database (booking, modifying flights, editing baggage, upgrading cabin class, or updating passenger information), you must list the action details and obtain explicit user confirmation (yes) to proceed.

- You should not provide any information, knowledge, or procedures not provided by the user or available tools, or give subjective recommendations or comments.

- You should only make one tool call at a time, and if you make a tool call, you should not respond to the user simultaneously. If you respond to the user, you should not make a tool call at the same time.

- You should deny user requests that are against this policy.

- You should transfer the user to a human agent if and only if the request cannot be handled within the scope of your actions.

## Domain Basic

- Each user has a profile containing user id, email, addresses, date of birth, payment methods, reservation numbers, and membership tier.

- Each reservation has an reservation id, user id, trip type (one way, round trip), flights, passengers, payment methods, created time, baggages, and travel insurance information.

- Each flight has a flight number, an origin, destination, scheduled departure and arrival time (local time), and for each date:
  - If the status is "available", the flight has not taken off, available seats and prices are listed.
  - If the status is "delayed" or "on time", the flight has not taken off, cannot be booked.
  - If the status is "flying", the flight has taken off but not landed, cannot be booked.

## Book flight

- The agent must first obtain the user id, then ask for the trip type, origin, destination.

- Passengers: Each reservation can have at most five passengers. The agent needs to collect the first name, last name, and date of birth for each passenger. All passengers must fly the same flights in the same cabin.

- Payment: each reservation can use at most one travel certificate, at most one credit card, and at most three gift cards. The remaining amount of a travel certificate is not refundable. All payment methods must already be in user profile for safety reasons.

- Checked bag allowance: If the booking user is a regular member, 0 free checked bag for each basic economy passenger, 1 free checked bag for each economy passenger, and 2 free checked bags for each business passenger. If the booking user is a silver member, 1 free checked bag for each basic economy passenger, 2 free checked bag for each economy passenger, and 3 free checked bags for each business passenger. If the booking user is a gold member, 2 free checked bag for each basic economy passenger, 3 free checked bag for each economy passenger, and 3 free checked bags for each business passenger. Each extra baggage is 50 dollars.

- Travel insurance: the agent should ask if the user wants to buy the travel insurance, which is 30 dollars per passenger and enables full refund if the user needs to cancel the flight given health or weather reasons.

## Modify flight

- The agent must first obtain the user id and the reservation id.

- Change flights: Basic economy flights cannot be modified. Other reservations can be modified without changing the origin, destination, and trip type. Some flight segments can be kept, but their prices will not be updated based on the current price. The API does not check these for the agent, so the agent must make sure the rules apply before calling the API!

- Change cabin: all reservations, including basic economy, can change cabin without changing the flights. Cabin changes require the user to pay for the difference between their current cabin and the new cabin class. Cabin class must be the same across all the flights in the same reservation; changing cabin for just one flight segment is not possible.

- Change baggage and insurance: The user can add but not remove checked bags. The user cannot add insurance after initial booking.

- Change passengers: The user can modify passengers but cannot modify the number of passengers. This is something that even a human agent cannot assist with.

- Payment: If the flights are changed, the user needs to provide one gift card or credit card for payment or refund method. The agent should ask for the payment or refund method instead.

## Cancel flight

- The agent must first obtain the user id, the reservation id, and the reason for cancellation (change of plan, airline cancelled flight, or other reasons)

- All reservations can be cancelled within 24 hours of booking, or if the airline cancelled the flight. Otherwise, basic economy or economy flights can be cancelled only if travel insurance is bought and the condition is met, and business flights can always be cancelled. The rules are strict regardless of the membership status. The API does not check these for the agent, so the agent must make sure the rules apply before calling the API!

- The agent can only cancel the whole trip that is not flown. If any of the segments are already used, the agent cannot help and transfer is needed.

- The refund will go to original payment methods in 5 to 7 business days.

## Refund

- If the user is silver/gold member or has travel insurance or flies business, and complains about cancelled flights in a reservation, the agent can offer a certificate as a gesture after confirming the facts, with the amount being $100 times the number of passengers.

- If the user is silver/gold member or has travel insurance or flies business, and complains about delayed flights in a reservation and wants to change or cancel the reservation, the agent can offer a certificate as a gesture after confirming the facts and changing or cancelling the reservation, with the amount being $50 times the number of passengers.

- Do not proactively offer these unless the user complains about the situation and explicitly asks for some compensation. Do not compensate if the user is regular member and has no travel insurance and flies (basic) economy.



# Policies from Salesforce


## Return Policy for Purchased Items: Guidelines for Hassle-Free Returns

At Shoes & Clothings, we strive to ensure that every athlete is fully satisfied with their purchase. Our commitment to quality and customer satisfaction extends to our return policy, designed to be clear, straightforward, and customer-friendly. Below, you'll find detailed guidelines to help you navigate the return process with ease. 

### Conditions for Return:
- **Time Frame:** Items must be returned within 30 days of the purchase date. Returns outside this window will not be accepted.

- **Condition:** Items should be unused, unwashed, and in their original packaging with all tags attached. Shoes must be returned in their original box. 
 
- **Receipt:** A valid proof of purchase, such as an original receipt or order confirmation email, is required for all returns. 

### Process for Initiating a Return:**
- **Online Purchases:** If you bought the item from our website, log in to your account and navigate to the 'Order History' section. Select the order you wish to return and click on 'Return Items.' Follow the on-screen instructions to complete the return request. 

- **In-Store Purchases:** If you purchased the item in one of our retail stores, bring the item along with your receipt to any Shoes & Clothings store. Our staff will assist you in processing the return.

- **Mail-In Returns:** For online purchases, you also have the option to mail the item back to us. Follow the return instructions provided with your order and use the prepaid return label included in your package. 

- **Refund Options:** 
  - **Full Refund:** If the return meets all conditions, you can opt for a full refund to your original payment method. Please allow 5-7 business days for the refund to be processed once we receive your returned item. 
  - **Store Credit:** If you prefer, you can choose to receive store credit, which can be used for future purchases at Shoes & Clothings, both online and in-store. 
  - **Exchange:** You may exchange the returned item for another product of equal or lesser value. If the new item costs more than the original one, you will need to pay the difference. 
  
- **Special Considerations:** 
  - **Defective Products:** If you receive a defective or damaged product, please contact our customer service team within 14 days of receipt. We will provide instructions for returning the defective item and ensure that you receive a replacement or a full refund. 
  - **Promotional Items:** Items purchased during special promotions or sales may be subject to different return conditions. Please check the terms of the promotion for specific return guidelines. 
  
- **Return Shipping Costs:** Shoes & Clothings covers the return shipping costs for domestic returns. For international returns, customers are responsible for the return shipping fees unless the item is defective or incorrect. By understanding our return policy, you can shop with confidence knowing that your satisfaction is our top priority. We are here to assist you through every step of the return process, ensuring a hassle-free experience.


## Resolving Product Mislabeling Issues: Steps and Solutions Provided by Shoes & Clothings

Ensuring that our customers receive the correct products is of utmost importance to us at Shoes & Clothings. Despite our best efforts, there may be rare instances where you receive an item with incorrect labeling. We deeply regret any inconvenience this may cause and are dedicated to resolving such issues promptly and efficiently. 

- **Step 1: Identifying the Mislabeling Issue** The first step is to carefully examine the item you received. Mislabeling can include incorrect size, style, color, or item description on the product label compared to your order. Ensure you cross-check the details on the label with the original order confirmation to identify any discrepancies

- **Step 2: Reporting the Issue** Once you've identified a mislabeling issue, it is essential to report it as soon as possible. Here’s how you can do it: 
  - **Contact Our Customer Service**: Reach out to our customer service team via phone, email, or live chat. Provide your order number, a clear description of the problem, and photographs of the item and its incorrect label. Visual evidence helps expedite the verification process. 
  - **Visit a Physical Store**: If you happen to be near one of our physical store locations, you can take the item directly to the store. Our store associates will assist you with the next steps and ensure your issue is recorded. 

- **Step 3: Verification Process** After you report the issue, our team will begin the verification process. This involves: 
  - **Reviewing Your Report**: Our customer service team will examine the details you've provided, including the photographs, order information, and a description of the issue. 
  - **Checking Inventory Records**: We will cross-reference your report with our inventory records to ensure the mislabeling claim is accurate. Once the mislabeling is confirmed, we will proceed to the resolution phase. 

- **Step 4: Solutions Offered** Shoes & Clothings is committed to customer satisfaction and offers the following solutions to rectify any mislabeling errors promptly: 
  - **Exchange for Correct Item**: If the item you received is mislabeled, we will arrange for an exchange. You can either visit one of our stores, where the correct item will be provided, or our customer service team can assist you in dispatching the correct item to your address at no extra cost. 
  - **Full Refund**: If an exchange is not feasible or the correct item is no longer available, we will offer a full refund for the mislabeled item. The refund will be processed using the original payment method, and you will receive confirmation once the transaction is completed. 
  - **Return Shipping**: In cases where you need to send back the mislabeled item, Shoes & Clothings will cover the return shipping costs. Our customer service team will provide you with a pre-paid return shipping label for your convenience. 

- **Commitment to Improvement** Shoes & Clothings continually strives to improve our processes to prevent such issues from occurring in the future. We conduct regular quality assurance checks and enhance our labeling protocols to minimize the chances of mislabeling. In conclusion, while it’s unfortunate when mislabeling occurs, rest assured that Shoes & Clothings is fully dedicated to resolving the issue swiftly and ensuring that you have a seamless shopping experience. Should you ever encounter this problem, follow the outlined steps, and our team will be ready to help you find a suitable and satisfactory resolution.


## Efficient Cancelation Policy for Orders at Shoes & Clothings

Cancelling an order at Shoes & Clothings is a streamlined process designed to ensure utmost convenience for our valued customers. Follow these guidelines to understand the time-sensitive steps, qualifying conditions, and how to obtain a refund or store credit efficiently. 

- **Time-Sensitive Steps:** To cancel an order, it’s crucial to act swiftly. You can cancel your order within a limited window after placing it, typically within the first 24 hours. This window may vary slightly depending on the specific items and current holiday or promotional schedules. We recommend checking your order confirmation email for precise details regarding cancellation windows. 

- **Qualifying Conditions:** Not all orders qualify for cancellation. Custom items, such as personalized products, may not be eligible due to the bespoke nature of these goods. Furthermore, orders that have already been processed for shipping cannot be canceled. If your order does not qualify for cancellation but you still wish to return the item, our standard return policy will apply. 

- **Cancellation Process:** To begin the cancellation process, follow these steps: 
  - **Visit Our Website**: Log into your account on the Shoes & Clothings website. 
  - **Access Order History**: Navigate to your order history to find the specific order you wish to cancel. 
  - **Request Cancellation**: Click on the order and select the cancellation option. You will be prompted to confirm your decision. 
  - **Confirmation Email**: Upon successfully submitting a cancellation request, you will receive a confirmation email outlining the details of your canceled order. If you encounter any issues or your order does not appear eligible for cancellation, please reach out to our customer service team for assistance. 
   
- **Customer Service Contact Points:** Our dedicated customer service team is available to help you with any cancellation inquiries. You can reach us through multiple channels: 
  - **Phone**: Call our customer service line for immediate support. 
  - **Email**: Send an email detailing your order number and cancellation request. Our team will respond promptly. 
  - **Live Chat**: Use the live chat feature on our website for real-time assistance. 
   
- **Obtaining a Refund or Store Credit:** After a successful cancellation, you will be entitled to a refund or store credit. The type of reimbursement depends on the original payment method and your preferences: 
  - **Credit/Debit Card**: Refunds will be processed back to the original card used for the purchase. Depending on your bank, this may take up to 5-7 business days to reflect in your account. 
  - **Store Credit**: If you prefer, you can opt for store credit instead of a direct refund. The store credit will be available in your Shoes & Clothings account for future purchases. 

By following these steps, you can ensure a smooth and hassle-free cancellation process at Shoes & Clothings. Our commitment to providing excellent customer service means that we are always here to help, making sure your experience is as seamless as possible.


## Understanding Shoes & Clothings' Exchange Policy: Seamless Swaps for Purchased Items

Understanding Shoes & Clothings' Exchange Policy: Seamless Swaps for Purchased Items At Shoes & Clothings, our goal is to provide an unparalleled shopping experience, which includes making sure you are completely satisfied with your purchase. Our streamlined exchange policy allows you to swap items effortlessly, ensuring the perfect fit, style, or functionality. Here, we'll guide you through the process of exchanging your purchased items, explaining the key steps and conditions to ensure a seamless experience.

- **Eligibility for Exchanges** To be eligible for an exchange, items must meet the following criteria: 
  - **Condition**: Items must be returned in their original condition, unworn, and with all original tags and packaging intact. 
  - **Time Frame**: Exchanges must be requested within 30 days of the original purchase date. 
  - **Proof of Purchase**: A valid receipt or order number must be provided to process the exchange. 
   
- **Steps to Exchange Your Item** 
  - **Initiate the Exchange Request** Visit our website and navigate to the "Order History" section under your account dashboard. Select the item you wish to exchange and click on "Request Exchange." If you made the purchase in-store, you can also initiate the exchange by visiting the store where you bought the item and speaking with a customer service representative.
  - **Select the Desired Item** When requesting an exchange online, you will be prompted to select the replacement item. You can choose a different size, color, or model depending on availability. If you are exchanging an item in-store, ensure to have the item you wish to exchange ready, and our staff will assist you in finding the perfect replacement. 
  - **Return the Original Item** For online exchanges, you will receive a prepaid return shipping label. Package the original item securely, attach the label, and drop it off at any authorized shipping location. If exchanging in-store, bring the original item with you. 
  - **Confirmation and Processing** Once we receive and inspect the original item, we will process your exchange. For online exchanges, you will receive an email confirmation once the new item has been shipped. For in-store exchanges, your new item will be provided to you during your visit. 
   
- **Conditions & Restrictions** 
  - **Limited Edition or Final Sale Items** Certain products, such as limited edition releases or items marked as final sale, may not be eligible for exchanges. Please refer to the product details or contact customer support for clarification. 
  - **Availability of Replacement Items** Exchanges are subject to the availability of the replacement item. If the desired item is out of stock, you will have the option to wait for restock, choose a different item, or opt for a refund. 
  - **International Exchanges** For international orders, please contact our customer service team for specific instructions, as the process may vary depending on the destination country. 
   
- **Customer Support** For any questions or assistance with your exchange, our customer support team is here to help. You can reach out via our website's live chat, email, or visit any Shoes & Clothings store for personalized assistance. 
 
In conclusion, Shoes & Clothings is committed to ensuring you are completely satisfied with your purchase, offering a straightforward and customer-friendly exchange policy. By following the steps and meeting the outlined conditions, you can confidently swap your items to achieve the perfect fit, color, or style.


## How to Redeem Loyalty Points for Discounts at Shoes & Clothings

How to Redeem Loyalty Points for Discounts at Shoes & Clothings At Shoes & Clothings, we value our loyal customers and offer an opportunity to redeem loyalty points for discounts on future purchases. If you're part of our loyalty program and are unsure how to turn your points into savings, this guide will walk you through the steps and options available.

- **Loyalty Points Credit**: One way to redeem your loyalty points is through the Loyalty Points Credit system. Here’s how it works:
  - **Earning Points**: You earn loyalty points with every qualifying purchase at Shoes & Clothings. Occasionally, points may also be added to your account as compensation for minor inconveniences or as part of special promotions. 
  - **Using Points**: These points accumulate in your account and can be redeemed for discounts on future purchases. There is no time limit for using these points, as they do not expire (valid_days = -1).
  - **Redemption Process**: To redeem your points, log into your Shoes & Clothings account on our website or mobile app. At checkout, select the option to apply your loyalty points. The corresponding discount will be automatically applied to your total purchase amount. 

- **Store Credit**: Another option for redeeming your loyalty rewards is through Store Credit, which provides a more flexible way to use your points: 
  - **Issuance of Credit**: Store Credit can be issued directly to your account, either as a reward for frequent purchases or as a response to service issues. 
  - **Validity**: Unlike Loyalty Points Credit, Store Credit has a validity period. It must be used within 90 days from the date it is issued (valid_days = 90). 
  - **Using Store Credit**: To use your Store Credit, simply log into your account and, during checkout, choose the option to apply Store Credit. The credit will then be deducted from your total purchase amount. 
   
- **Important Reminders**: 
  - **Eligibility**: Ensure you are logged into your registered account where your loyalty points and store credits are accumulated. 
  - **Monitoring Balance**: Regularly check your points and credit balance to maximize your rewards. 
  - **Expiration**: Be mindful of the expiration date for Store Credit (90 days), and use it before it expires to avoid losing your rewards. 
 
By understanding these two methods of redeeming your loyalty points – Loyalty Points Credit and Store Credit – you can make the most of your purchases at Shoes & Clothings. Whether you prefer the timeless flexibility of loyalty points or the immediate benefit of store credit, both options are designed to reward your loyalty and enhance your shopping experience. Start redeeming your points today and enjoy the benefits of our loyalty program!


## How to Handle Order Cancellation Issues with Shoes & Clothings

Handling Order Cancellation Issues with Shoes & Clothings If you encounter difficulties canceling your order on the Shoes & Clothings website, rest assured there are effective solutions available. Below, we outline the steps you can take to address this issue and ensure a smooth resolution. 

- **Check Cancellation Window**: Verify that your order is indeed within the cancellation window. Orders are typically eligible for cancellation within a specific time frame after the purchase is made. This information can usually be found in your order confirmation email or on your Shoes & Clothings account.

- **Full Refund**: If you are unable to cancel your order online but are still within 30 days of the purchase date, you may be eligible for a full refund. This solution is ideal if the items you ordered are damaged, incorrect, or otherwise unsatisfactory. To pursue a full refund, contact our customer service team with your order number and details about the issue. Our team will process the refund, including any shipping fees, making sure you are reimbursed promptly. 

- **Store Credit**: Alternatively, you may opt for store credit, which can be a convenient way to manage future purchases if you decide not to get a direct refund. This solution is available within 90 days of the purchase date and will be credited to your Shoes & Clothings account. Store credit is valid for future purchases and can be a flexible option if you plan to shop with us again. To request store credit, reach out to customer service with your order information, and they will facilitate the credit transfer to your account. 

- **Contacting Customer Service**: If you are within the eligible time frames for either a full refund (30 days) or store credit (90 days), and find yourself unable to cancel the order online, direct communication with our customer service is key. Provide them with your order details, including the order number, date of purchase, and the reason for cancellation. 
 
Our team is committed to resolving your issue efficiently, ensuring you have a hassle-free shopping experience. Remember, our goal at Shoes & Clothings is to provide you with the best possible service and support, so do not hesitate to reach out if you face any challenges. Your satisfaction is our priority, and we will work diligently to resolve any order cancellation issues you encounter.


## Addressing Shipping Delays: Solutions for Enhanced Customer Satisfaction

Addressing a two-week delay on an order originally promised within 3-5 days is crucial for maintaining customer satisfaction and loyalty. At Shoes & Clothings, we understand the frustration this can cause and are committed to providing customer-centric solutions to mitigate any inconvenience. Below are the initiatives we offer to compensate for such delays and enhance your overall shopping experience: 

- **Loyalty Points Credit** Adding loyalty points to your account is our way of showing appreciation for your patience and ongoing support. These points can be accumulated and redeemed against future purchases, rewarding you for sticking with us even through minor inconveniences. There is no expiration date for these loyalty points, allowing you the flexibility to use them whenever you choose. This solution is ideal for customers who frequently shop with us and enjoy the benefits of our loyalty program. 

- **Store Credit** We also offer store credit as a tangible way to apologize for the delay. This credit, which will be added to your account, can be used toward any future purchases at Shoes & Clothings. The store credit is valid for 90 days after issuance, giving you ample time to find the perfect item to use it on. This solution is particularly useful for customers who have an upcoming purchase in mind or are waiting for a restock of their favorite items. 

- **Free Shipping on Next Order** To make up for the inconvenience, we extend free shipping on your next order. This gesture of goodwill is valid for 180 days, providing you with plenty of time to make your next purchase without worrying about additional shipping charges. This solution is beneficial for customers who frequently order online and wish to save on shipping costs in the future. 

- **Exclusive Discount Code** Another effective solution is providing an exclusive discount code for your next purchase. This discount code is valid for 60 days and offers a special reduced rate on any item of your choice. It serves as an incentive to continue shopping with us and allows you to make additional purchases at a lower cost. This option works well for customers who are looking to make another purchase soon and wish to benefit from added savings. 
 
By offering these solutions, Shoes & Clothings ensures our customers feel valued and appreciated despite any shipping delays. We strive to turn any inconvenience into an opportunity to enhance your shopping experience and reinforce our commitment to customer satisfaction.


## Addressing Product Defects: Ensuring Quality Footwear from Shoes & Clothings

At Shoes & Clothings, we pride ourselves on delivering top-quality products that meet the rigorous demands of our customers and help them achieve their athletic goals. Nevertheless, despite our stringent quality control processes, there may be rare instances where a product defect occurs. In this article, we address a specific issue where a customer received a pair of running shoes with a damaged sole that came apart after only a week of use. To resolve such issues and ensure customer satisfaction, we offer two primary solutions: a full refund or a replacement of the defective product. 

- **Full Refund** If you received a defective pair of running shoes, you have the option to request a full refund. This solution is designed to provide a complete refund for the purchase amount, including any shipping fees. Customers can opt for this solution if the shoes are damaged or incorrect. To be eligible for a full refund, you must submit your request within 30 days of the purchase date. Our customer service team will guide you through the process to ensure a swift resolution, and your funds will be returned to the original method of payment used during the purchase. This option is particularly suitable for customers who prefer to receive their money back rather than a replacement product. 

- **Replacement** Alternatively, if you prefer to receive a replacement for the defective pair of running shoes, we offer a solution to send you a new product. This option ensures that you receive a fully functional pair of shoes that meet our quality standards, allowing you to return to your athletic pursuits without further delay. Customers can request a replacement within 60 days of the purchase date. Once your request is verified and processed, a new pair of running shoes will be shipped to you at no additional cost. This solution is ideal for those who wish to continue using the same model and style of footwear that initially appealed to them. 
 
In conclusion, we at Shoes & Clothings are committed to upholding our promise of delivering high-quality athletic footwear to all our customers. By offering solutions such as a full refund or a replacement within specified time frames, we aim to address any product defects that may arise and ensure complete customer satisfaction. Should you encounter any issues with your purchase, our customer service team is available to assist you and provide the support needed to resolve the matter promptly. Thank you for choosing Shoes & Clothings and for your understanding and cooperation in ensuring an excellent customer experience.

