# Roadmap for DocsInARow

This document outlines upcoming features and enhancements for DocsInARow.

## Version 0.2.0 (Q3 2023)

### New Features

1. **Multi-user Support**: Expand the application capabilities to accommodate multi-user homes, allowing different users to scan and categorize their documents separately.

2. **Automatic Document Categorization**: Improve the application to automatically categorize documents into different types (invoices, receipts, letters etc.) based on the contents.

3. **Email Reports**: Implement a feature that generates a report of processed documents, including brief descriptions, importance ranking, and viewing links, and then email this report to users regularly.

### Enhancements

1. **Improved OCR Accuracy**: Work on enhancing the OCR capabilities to ensure better accuracy when reading documents.

2. **Support for More File Formats**: Add support for PDFs and other image formats (like PNG, TIFF).

3. **Cross-platform Support**: Enhance DocsInARow to work seamlessly across Windows, macOS, and Linux systems.

4. **Background Service**: Transform DocsInARow into a service that continuously monitors a specified directory, processes new documents as they arrive, and impose a limit on the number of documents processed per day to manage API costs.

5. **Improved Error Handling**: Improve error handling throughout the application to make it more robust and user-friendly.

## Version 0.3.0 (Q4 2023)

### New Features

1. **Local Data Encryption**: Implement encryption for the locally stored data to protect against unauthorized access.

2. **Secure Data Transmission**: Ensure that all data transmitted over networks is properly encrypted to prevent data leaks during transmission.

3. **PII Scrubber**: Develop a local processing tool to identify and scrub out personally identifiable information (PII) from documents before they are processed by cloud-based services. This tool would be able to recognize and remove common types of PII like names, addresses, social security numbers, etc.

## Version 0.4.0 (Q1 2024)

### New Features

1. **Integration with Cloud Storage**: Allow the application to pull documents from cloud storage services like Google Drive or Dropbox.

2. **Support for Non-English Languages**: Expand the application to support document categorization for non-English languages.

3. **Bulk Processing**: Add a feature to process multiple images at once, without asking for confirmation after each image.

4. **Integrate into AI assistant tools** to allow AI assistants to know and understand the documents relevant to your life to better assist you in your day to day

### Enhancements

1. **UI/UX Improvements**: Implement improvements to the user interface and overall user experience.

2. **Secure Cloud Storage Integration**: Integrate with cloud storage services in a secure manner, ensuring data is encrypted before it is uploaded, and access control policies are robust.

## Version 0.5.0 (Q2 2024)

### New Features

1. **Data Anonymization and Pseudonymization**: Implement data anonymization and pseudonymization features to prevent personal data from being visible in processed data.

2. **Security Audit and Compliance Features**: Introduce features to facilitate security auditing and compliance with privacy laws and guidelines.

## Enhancements

3. **Improved Access Controls**: Enhance user management features and access controls to ensure only authorized users have access to the appropriate data.


Please note, this roadmap is subject to changes. New ideas and contributions are always welcome!

## Version 1.0.0 (Q4 2023)

### New Features

1. **Paid Version**: Develop a user-friendly, subscription-based version of DocsInARow which simplifies setup through a graphical user interface (GUI), automates API key configuration, and provides enhanced features through a cloud-backed infrastructure.

2. **Document Organization Flexibility**: Add the ability for users to customize their document organization method based on their preference.

3. **Integration with External APIs**: Allow users to connect with third-party services, such as billing or project management software, for easy sharing and collaboration.

4. **Accessibility Features**: Implement features that make the application more accessible to people with disabilities.

### Enhancements

1. **Performance Optimizations**: Optimize the application for better performance when processing large documents or large batches of documents.

2. **Enhanced Security Measures**: Increase security measures to protect user data, especially for the subscription-based version.
