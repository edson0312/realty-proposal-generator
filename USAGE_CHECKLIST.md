# 📋 Moldex Realty Sample Computation - Usage Checklist

Use this checklist when generating proposals for clients.

---

## 🚀 Before You Start

- [ ] Application is running (visit http://localhost:5000)
- [ ] Client information is ready
- [ ] Property details are available
- [ ] Pricing information confirmed
- [ ] Property photo ready (if available)

---

## 📝 Required Information

### Client Details (All Required)
- [ ] Client's full name
- [ ] Valid email address
- [ ] Contact number (optional but recommended)

### Project Details (Required)
- [ ] Product Type selected (Vertical or Horizontal)
- [ ] Project Type selected
- [ ] Property location/address
- [ ] Brand name
- [ ] Property measurements (floor area, lot area, etc.)

### Contract Details (All Required)
- [ ] Total Contract Price (TCP) entered
- [ ] Reservation Fee amount
- [ ] Registration Fee percentage
- [ ] Move-in Fee percentage

### Payment Terms (At Least One Required)
- [ ] At least one payment term is filled out:
  - [ ] Spot Cash discount percentage OR
  - [ ] Deferred Payment term(s) OR
  - [ ] Spot Down Payment details OR
  - [ ] 20/80 Payment terms

---

## 🎯 Step-by-Step Form Completion

### Step 1: Client Details
1. [ ] Enter client's name
2. [ ] Enter email address
3. [ ] Enter contact number (if available)

### Step 2: Product Selection
4. [ ] Select Product Type (Vertical or Horizontal)

### Step 3A: If Vertical Selected
5. [ ] Select Project Type (Mid Rise or High Rise Building)
6. [ ] Enter Brand name
7. [ ] Enter Address
8. [ ] Enter Tower/Building
9. [ ] Enter Floor/Unit
10. [ ] Enter Floor Area
11. [ ] Upload property picture (optional)

### Step 3B: If Horizontal Selected
5. [ ] Select Project Type (House and Lot or Lot)
6. [ ] Enter Brand name
7. [ ] Enter Address
8. [ ] Enter Phase
9. [ ] Enter Block/Lot

**If House and Lot:**
10. [ ] Enter House Model
11. [ ] Enter Property Details
12. [ ] Enter Lot Area
13. [ ] Enter Floor Area
14. [ ] Upload property picture (optional)

**If Lot Only:**
10. [ ] Enter Lot Area
11. [ ] Upload property picture (optional)

### Step 4: Contract Details
12. [ ] Enter Total Contract Price (numbers only)
13. [ ] Enter Reservation Fee
14. [ ] Enter Registration Fee % (e.g., 6)
15. [ ] Enter Move-in Fee % (e.g., 1.5)
16. [ ] Verify auto-calculated fees are displayed

### Step 5: Payment Terms (Choose as many as applicable)

#### Spot Cash
17. [ ] Enter Discount % (if offering spot cash)
18. [ ] Verify Discount Amount is calculated
19. [ ] Verify Net TCP is calculated

#### Deferred Payment
20. [ ] Enter Term 1 in months (e.g., 12)
21. [ ] Enter Term 2 in months (optional, e.g., 18)
22. [ ] Enter Term 3 in months (optional, e.g., 24)

#### Spot Down Payment
23. [ ] Enter Discount %
24. [ ] Verify 80% Balance is calculated
25. [ ] Enter Term 1 in years (e.g., 5)
26. [ ] Enter Rate 1 in % (e.g., 10)
27. [ ] Enter Term 2 in years (optional)
28. [ ] Enter Rate 2 in % (optional)
29. [ ] Enter Term 3 in years (optional)
30. [ ] Enter Rate 3 in % (optional)

#### 20/80 Payment Terms
31. [ ] Verify 20% calculations are displayed
32. [ ] Enter Term 1 in months for 20% (e.g., 12)
33. [ ] Enter Term 2 in months (optional)
34. [ ] Enter Term 3 in months (optional)
35. [ ] Verify 80% Balance is calculated
36. [ ] Enter Term 1 in years for 80% (e.g., 10)
37. [ ] Enter Rate 1 in %
38. [ ] Enter additional 80% terms if needed (optional)

### Step 6: Generate Proposal
39. [ ] Scroll to bottom of form
40. [ ] Review all entered information
41. [ ] Click "Generate Proposal" button
42. [ ] Wait for processing (2-3 seconds)
43. [ ] Look for success message
44. [ ] Click download link in success message
45. [ ] Save PDF to desired location

---

## ✅ Quality Check After Generation

### Review the PDF
- [ ] Client name is correct
- [ ] Contact information is accurate
- [ ] Property details are complete
- [ ] TCP and fees are correct
- [ ] All selected payment terms are included
- [ ] Calculations appear correct
- [ ] Property picture is included (if uploaded)
- [ ] Document looks professional
- [ ] Disclaimer section is present
- [ ] Signature areas are clear

### Verify Calculations
- [ ] Registration Fee = (TCP ÷ 1.12) × Registration %
- [ ] Move-in Fee = (TCP ÷ 1.12) × Move-in %
- [ ] Spot Cash Net TCP = (TCP - Discount) - Reservation Fee
- [ ] 20% calculations are correct
- [ ] 80% balance calculations are correct
- [ ] Monthly amortizations make sense

---

## 🔄 If You Need to Make Changes

### Minor Corrections
1. [ ] Go back to browser
2. [ ] Make necessary changes in form
3. [ ] Click "Generate Proposal" again
4. [ ] New PDF will be generated

### Major Changes
1. [ ] Refresh the page to start fresh
2. [ ] Re-enter all information
3. [ ] Generate new proposal

---

## 💾 File Management

### After Successful Generation
- [ ] PDF is saved in `uploads` folder
- [ ] Filename includes client name and timestamp
- [ ] File can be sent to client via email
- [ ] Keep a copy for records

### Regular Maintenance
- [ ] Periodically backup the `uploads` folder
- [ ] Archive old proposals
- [ ] Delete test/duplicate files

---

## ⚠️ Common Mistakes to Avoid

### Data Entry
- [ ] Don't use commas in number fields (use 8000000, not 8,000,000)
- [ ] Don't include currency symbols in price fields
- [ ] Don't leave required fields empty
- [ ] Don't forget to click Generate button

### Payment Terms
- [ ] Don't enter monthly terms in year fields
- [ ] Don't forget the decimal in percentages (use 6, not 0.06)
- [ ] Don't mix up Registration % and Move-in %
- [ ] Don't forget to fill at least one payment term

### File Upload
- [ ] Don't upload files larger than 16MB
- [ ] Don't upload unsupported file types
- [ ] Don't use special characters in filenames
- [ ] Don't upload corrupt or damaged images

---

## 🆘 Troubleshooting Quick Reference

### Problem: Form won't submit
- [ ] Check all required fields are filled (marked with *)
- [ ] Verify TCP is greater than 0
- [ ] Ensure at least one payment term is filled
- [ ] Check browser console for errors

### Problem: PDF download fails
- [ ] Check that success message appeared
- [ ] Verify download link is clickable
- [ ] Check browser's download folder
- [ ] Try right-click > Save As on download link

### Problem: Calculations seem wrong
- [ ] Verify you entered percentages correctly (6, not 0.06)
- [ ] Check TCP amount is correct
- [ ] Review formula in COMPUTATION_FORMULAS.md
- [ ] Run test_computations.py to verify system

### Problem: Picture not appearing in PDF
- [ ] Verify file was uploaded successfully
- [ ] Check file format (JPG, PNG, GIF, WEBP only)
- [ ] Ensure file size is under 16MB
- [ ] Try a different image file

---

## 📊 Sample Values for Testing

Use these values to test the system:

```
Client Name: Juan Dela Cruz
Email: juan.delacruz@email.com
Contact: 0917-123-4567

Product Type: Vertical
Project Type: Mid Rise Building
Brand: The Premiere
Address: Pasig City, Metro Manila
Tower/Building: Tower A
Floor/Unit: 15th Floor, Unit 1503
Floor Area: 45 sqm

TCP: 4013000
Reservation Fee: 50000
Registration Fee %: 6
Move-in Fee %: 1.5

Spot Cash Discount: 5
Deferred Terms: 12, 24
Spot Down Discount: 5
Spot Down 80% Terms: 10 years at 10%
20/80 Terms: 12, 24 months
20/80 80% Terms: 10 years at 10%
```

---

## 📈 Best Practices

### For Agents
1. [ ] Always verify client information before generating
2. [ ] Keep a copy of all generated proposals
3. [ ] Follow up with clients within 24 hours
4. [ ] Update pricing information regularly
5. [ ] Check computation accuracy periodically

### For Managers
1. [ ] Review sample proposals weekly
2. [ ] Verify formulas are still accurate
3. [ ] Keep system updated and maintained
4. [ ] Train new agents on proper usage
5. [ ] Collect feedback for improvements

### For IT/Admin
1. [ ] Backup uploads folder regularly
2. [ ] Monitor disk space usage
3. [ ] Check application logs for errors
4. [ ] Update dependencies when needed
5. [ ] Test after any system changes

---

## 📞 Need Help?

**Documentation:**
- README.md - Complete guide
- SETUP_GUIDE.txt - Setup instructions
- COMPUTATION_FORMULAS.md - Formula reference
- PROJECT_SUMMARY.md - Overview

**Testing:**
- Run: `python test_computations.py`

**Support:**
- Contact your system administrator
- Check application logs
- Review error messages

---

## ✨ Tips for Success

1. **Prepare First**: Gather all information before starting
2. **Double Check**: Review entries before generating
3. **Test First**: Use sample data to familiarize yourself
4. **Save Copies**: Keep PDFs for your records
5. **Be Consistent**: Use same format for all clients
6. **Stay Updated**: Check for system updates regularly

---

**Version:** 1.0.0  
**Last Updated:** November 11, 2024

Happy Generating! 🎉

